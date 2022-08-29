"""
A sample RNN to learn superposition of dumping pulses
Note: SL must be at least equal to MPH, to make the problem mathematically solvable
"""
import os
import pathlib
from datetime import datetime
import json
import shutil

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from RNN_for_dumped_pulses.settings import (
    LOG_FILENAME,
    CHECKPOINT_SUBFOLDER, LOCAL_CHECKPOINT_FILENAME,
    CONFIG_FILE, SAVED_RNN_DIR
)
from RNN_for_dumped_pulses.config_example import *

from tensorflow import data
from keras import layers, models, callbacks, losses, optimizers

# todo: let's try ConfigParser too...
RNN_INFO_FOLDER = SAVED_RNN_DIR / f"RNN_{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"
os.makedirs(RNN_INFO_FOLDER, exist_ok=True)
# load parameters:
with open(CONFIG_FILE, encoding='utf-8') as f:
    parameters = json.load(f)
for p, v in parameters.items():
    exec(f'{p}={v}')
# save parameters:
shutil.copyfile(src=CONFIG_FILE, dst=RNN_INFO_FOLDER / 'config.json')
del f, parameters, p, v


def create_dumping_pulse(n: int,
                         max_pulse: bool = False) -> np.array:
    """
    This creates a positive pulse n-high with a linear decay of 45° slope (= saw-tooth pulse)

    :param n: the height of the pulse
    :param max_pulse: if True n = MPH
    :return:
    """
    n = min(n, MPH) if not max_pulse else MPH
    x = np.arange(n + 1)
    y = np.flip(x)
    return y


def compute_influx(pulse_heights: np.array,
                   sample_plot: bool = False,
                   **kwargs) -> np.array:
    """

    :param pulse_heights: an array of pulse height
    :param sample_plot: if True plots the sawtooths
    :param kwargs: max_pulse
    :return:
    """
    n = len(pulse_heights)
    _effect = np.zeros(n + MPH * 2)
    for i in range(n):
        single_influx = create_dumping_pulse(pulse_heights[i], **kwargs)
        _effect[i: i + len(single_influx)] += single_influx
        if sample_plot and i <= MAX_PULSE_TO_PLOT:
            x_stream = np.zeros(n + MPH * 2)
            x_stream[i: i + len(single_influx)] = single_influx
            plt.plot(x_stream)
            plt.show()
    return _effect[:n]


def generate_effect_simulation(**kwargs):
    """

    :param kwargs: max_pulse, sample_plot
    :return:
    """
    pulses_train = np.random.randint(MPH + 1, size=N)
    influx = compute_influx(pulses_train, **kwargs)
    return pulses_train, influx


def prepare_training_set(x, y,
                         sl: int = SL,
                         variable_len: bool = False):
    """
    Prepare the training sample of shape (Batch_dim, time_steps, 1)
    timesteps will be equal to sl
    We will then have a bunch of sl-length arrays

    :param x: pulses
    :param y: effects
    :param sl: the number of pulses from a single input sequence. They are the minimum number of pulses
        mathematically necessary to predict the effect.
    :param variable_len: if True, pulses' inputs will have variable length between 'sl' and '2*sl',
        plus they will be 0-left-padded. If False, every sequence will be 'sl'-length
    :return:
    """
    from sklearn.model_selection import train_test_split
    if variable_len:
        sequences, y_hat = [], []
        max_len = 2 * sl
        max_index = len(x) - max_len
        for current_len in range(sl, max_len + 1):
            variable_l_sequences = np.asarray(
                [x[i: i + current_len] for i in range(max_index)]
            )  # maybe there is a more performat way here to vectorise
            # maybe it's possible to use numpy diff for this generation
            variable_l_y_hat = y[(current_len - 1): (current_len - 1) + max_index]
            padding_length = max_len - current_len
            variable_l_sequences = np.pad(
                variable_l_sequences, ((0, 0), (padding_length, 0)), 'constant'
            )  # padding left with zeros
            sequences.append(variable_l_sequences)
            y_hat.append(variable_l_y_hat)
        sequences = np.concatenate(sequences, axis=0)
        y_hat = np.concatenate(y_hat, axis=0)
    else:
        max_len = sl
        max_index = len(x) - max_len + 1
        sequences = np.asarray([x[i: i + sl] for i in range(max_index)])
        y_hat = y[(sl - 1):]
    _X_train, _X_test, _Y_train, _Y_test = train_test_split(sequences, y_hat,
                                                            test_size=0.2,
                                                            random_state=1,
                                                            shuffle=True,
                                                            stratify=None)
    return sequences, y_hat, _X_train, _X_test, _Y_train, _Y_test


def convert_dataset_to_tf_dataset(x_train, y_train):
    dataset = data.Dataset.from_tensor_slices((x_train, y_train))
    dataset = dataset.batch(batch_size=BATCH_SIZE)
    prepared_dataset = dataset.shuffle(buffer_size=x_train.shape[1], reshuffle_each_iteration=True)
    return prepared_dataset


def learn_with_rnn(dataset):
    # 1. BUILD RNN ARCHITECTURE:
    def expand_dimension(x):
        from tensorflow import expand_dims
        return expand_dims(x, axis=-1)

    model = models.Sequential(
        [
            layers.Lambda(expand_dimension,
                          input_shape=[None]),
            layers.LSTM(units=64, activation='tanh'),
            layers.Dense(units=1)  # try also "swish". This neuron has no activation f.
        ]
    )
    optimizer = optimizers.Adam(learning_rate=INITIAL_LEARNING_RATE)
    loss = losses.MeanAbsoluteError()
    metrics = ["mae"]
    model.compile(loss=loss,
                  optimizer=optimizer,
                  metrics=metrics)

    # 2. SET TRAINING PARAMETERS AND CALLBACKS:
    reduce_lr = callbacks.ReduceLROnPlateau(monitor='loss', factor=0.3,
                                            patience=5, min_lr=1e-9,
                                            verbose=1, mode='min', min_delta=0.3)
    csv_logger = callbacks.CSVLogger(RNN_INFO_FOLDER / LOG_FILENAME, append=True)
    checkpoint_path = RNN_INFO_FOLDER / CHECKPOINT_SUBFOLDER / LOCAL_CHECKPOINT_FILENAME
    cp_callback = callbacks.ModelCheckpoint(
        filepath=checkpoint_path,
        verbose=1,
        save_weights_only=True,
        save_freq='epoch',
        period=3
    )
    es_callback = callbacks.EarlyStopping(monitor='loss', patience=5, verbose=0)

    # 3. TRAIN THE RNN
    history = model.fit(dataset,
                        epochs=EPOCHS,
                        shuffle=True,
                        callbacks=[reduce_lr, csv_logger, cp_callback, es_callback]
                        )

    # 4. SAVE THE MODEL
    model.save(RNN_INFO_FOLDER)
    return history
    # todo: see if we can use the tensorflow method in the post for saving and loading, without having to do things
    #  directly with the keras framework.
    # todo: add use of tensorboard
    # todo: evaluate with the test set now!!


def use_saved_model(subfolder: pathlib.Path):
    folder = SAVED_RNN_DIR / subfolder
    model = models.load_model(folder)
    history = pd.read_csv(folder / LOG_FILENAME)
    plt.plot(history.epoch, history.mae)
    return model


def predict_value(sequence: list,
                  model: models):
    # the last value of the ground truth array should be the one matching the prediction
    sequence_padded = [0] * (MPH * 2 - len(sequence)) + sequence
    ground_truth = compute_influx(sequence)
    prediction = model.predict([sequence_padded])
    print('sequence_padded', sequence_padded)
    print('ground truth', ground_truth)
    print('prediction', prediction)
    return sequence_padded, ground_truth, prediction


if __name__ == '__main__':
    pulses, effects = generate_effect_simulation(sample_plot=False,
                                                 max_pulse=False)

    if PLOT_EFFECTS:
        plt.plot(effects)
    all_x, all_y, X_train, X_test, Y_train, Y_test = prepare_training_set(pulses, effects,
                                                                          variable_len=True)
    this_dataset = convert_dataset_to_tf_dataset(X_train, Y_train)
    model_history = learn_with_rnn(this_dataset)
    model_history.model.evaluate(X_test, Y_test, return_dict=True)
    plt.plot(model_history.epoch, model_history.history['loss'])
