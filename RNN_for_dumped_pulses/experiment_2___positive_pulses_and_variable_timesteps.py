"""
A sample RNN to learn superposition of pulses that dump over
"""
import os
from datetime import datetime

import numpy as np
from matplotlib import pyplot as plt
from RNN_for_dumped_pulses.settings import WORKING_DIR, LOG_FILENAME, CHECKPOINT_SUBFOLDER, LOCAL_CHECKPOINT_FILENAME
from tensorflow import data, TensorSpec, as_dtype
from keras import layers, models, callbacks, losses, optimizers

# ***** parameters for pulses' generation
N = 1000  # number of pulses generated (data points)
MPH = 10  # max pulse height
SL = MPH   # sequence length: number of time steps passed each time to the RNN
RANDOM_LEN = True   # sequences are created with random length between SL and 2*SL
MAX_PULSE_TO_PLOT = 200
# ***** parameters for RNN
TRAIN_FRACTION = 0.8
EPOCHS = 2  # 5 is for demo purpose. Set this parameter to 1000 for a real (long) run
BATCH_SIZE = 256
INITIAL_LEARNING_RATE = 5 * 1e-5


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


def prepare_vl_training_set(x, y, sl: int = SL):
    """
    Prepare the training sample of shape (Batch_dim, time_steps, 1)
    timesteps will be equal to sl
    We will then have a bunch of sl-length arrays

    :param variable_len:
    :param sl:
    :param x:
    :param y:
    :return:
    """
    from sklearn.model_selection import train_test_split
    variable_l_sequences, variable_l_y_hat = [], []
    for max_len in range(sl, 2*sl):
        max_len = sl
        max_index = len(x) - max_len + 1
        sequences = np.asarray([x[i: i + sl] for i in range(max_index)])
        y_hat = y[(sl - 1):]
        variable_l_sequences.append(sequences)
        variable_l_y_hat.append(y_hat)
    _X_train, _X_test, _Y_train, _Y_test = train_test_split(variable_l_sequences,
                                                            variable_l_y_hat,
                                                            test_size=0.2,
                                                            random_state=1,
                                                            stratify=None)
    return variable_l_sequences, variable_l_y_hat, _X_train, _X_test, _Y_train, _Y_test


def convert_dataset_to_tf_dataset(x_train, y_train):
    dataset = data.Dataset.from_tensor_slices((x_train, y_train))
    dataset = dataset.batch(batch_size=BATCH_SIZE)
    # todo: is this working with x_train.shape[1] ???
    prepared_dataset = dataset.shuffle(buffer_size=x_train.shape[1], reshuffle_each_iteration=True)
    return prepared_dataset


def convert_vl_dataset_to_tf_dataset(x_train, y_train):
    dataset = data.Dataset.from_generator(
        lambda: zip(x_train, y_train),
        output_signature=(
            TensorSpec([None, ], dtype=as_dtype(x_train[0].dtype)),
            TensorSpec([], dtype=as_dtype(y_train.dtype))
        )
    )
    prepared_dataset = dataset.shuffle(buffer_size=x_train.shape[0], reshuffle_each_iteration=True)
    return prepared_dataset


def learn_with_rnn(dataset):
    # 1. BUILD RNN ARCHITECTURE:
    def expand_dimension(x):
        from tensorflow import reshape
        return reshape(x, [None, None, x.shape[0]])
        # return expand_dims(x, axis=-1)

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
    rnn_info_folder = WORKING_DIR / f"RNN_{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"
    os.makedirs(rnn_info_folder, exist_ok=True)
    reduce_lr = callbacks.ReduceLROnPlateau(monitor='loss', factor=0.3,
                                            patience=5, min_lr=1e-9,
                                            verbose=1, mode='min', min_delta=0.3)
    csv_logger = callbacks.CSVLogger(rnn_info_folder / LOG_FILENAME, append=True)
    checkpoint_path = rnn_info_folder / CHECKPOINT_SUBFOLDER / LOCAL_CHECKPOINT_FILENAME
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
    model.save(rnn_info_folder)
    return history
    # todo: add use of tensorboard
    # todo: evaluate with the test set now!!
    # todo: fix the bug to save the model!


def learn_with_rnn_not_using_datasets(x_train, y_train):
    model = models.Sequential(
        [
            layers.LSTM(units=64, activation='tanh', input_shape=(None, 1)),
            layers.Dense(units=1)  # try also "swish". This neuron has no activation f.
        ]
    )
    model.compile()
    history = model.fit(x=x_train, y=y_train)
    return history


if __name__ == '__main__':
    pulses, effects = generate_effect_simulation(sample_plot=False,
                                                 max_pulse=False)
    all_x, all_y, X_train, X_test, Y_train, Y_test = prepare_vl_training_set(pulses, effects)
