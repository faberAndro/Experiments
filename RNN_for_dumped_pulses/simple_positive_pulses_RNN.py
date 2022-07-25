"""
A sample RNN to learn superposition of pulses that dump over
"""

import numpy as np
from matplotlib import pyplot as plt
from RNN_for_dumped_pulses.settings import DRIVE_DIR, LOG_FILE, CHECKPOINT_FILE, LOCAL_SAVING_DIR, \
    LOCAL_CHECKPOINT_FILE, LOCAL_LOG_FILE

# np.random.seed(8)   # for repeatibility in pulses random generation

# ***** parameters for pulses' generation
N = 50000   # number of pulses generated (data points)
MPH = 10  # max pulse height
MAX_PULSE_TO_PLOT = 200

# ***** parameters for RNN
TRAIN_FRACTION = 0.8
BATCH_SIZE = 128
EPOCHS = 30       # 5 is for demo purpose. Set this parameter to 1000 for a real (long) run
RNN_OUTPUT_FACTOR_CORRECTION = 1000.0
INITIAL_LEARNING_RATE = 5*1e-5


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
    _effect = np.zeros(n + MPH*2)
    for i in range(n):
        single_influx = create_dumping_pulse(pulse_heights[i], **kwargs)
        _effect[i: i + len(single_influx)] += single_influx
        if sample_plot and i <= MAX_PULSE_TO_PLOT:
            x_stream = np.zeros(n + MPH*2)
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


def prepare_training_set(x, y):
    """
    Prepare the training sample of shape (Batch_dim, time_steps, 1)
    timesteps will be equal to MPH
    We will then have a bunch of MPH-length arrays

    :param x:
    :param y:
    :return:
    """
    from sklearn.model_selection import train_test_split
    max_index = len(x) - MPH + 1
    # creates all the possible (and ordered) sequences from the training sample.
    sequences = np.asarray([x[i: i + MPH] for i in range(max_index)])
    y_hat = y[(MPH - 1):]
    _X_train, _X_test, _Y_train, _Y_test = train_test_split(sequences, y_hat,
                                                            test_size=0.2,
                                                            random_state=1,
                                                            shuffle=True,
                                                            stratify=None)

    return sequences, y_hat, _X_train, _X_test, _Y_train, _Y_test


def learn_with_rnn(X_train, X_test, Y_train, Y_test):
    import tensorflow as tf

    # 1. BUILD RNN ARCHITECTURE:
    model = tf.keras.models.Sequential(
        [
            tf.keras.layers.Lambda(lambda x: tf.expand_dims(x, axis=-1),
                                   input_shape=[None]),
            tf.keras.layers.LSTM(units=64, activation='tanh'),
            tf.keras.layers.Dense(units=1),     # try also "swish. This neuron has no activation f."
            # tf.keras.layers.Lambda(lambda x: x * RNN_OUTPUT_FACTOR_CORRECTION)
        ]
    )
    optimizer = tf.keras.optimizers.Adam(lr=INITIAL_LEARNING_RATE)
    loss = tf.keras.losses.MeanAbsoluteError()
    metrics = ["mae"]
    model.compile(loss=loss,
                  optimizer=optimizer,
                  metrics=metrics)

    # 2. SET DATA SAVE & CHECKPOINTS
    # model.save('my_model')
    checkpoint_path = str(LOCAL_SAVING_DIR / LOCAL_CHECKPOINT_FILE.format(epoch=0))
    # model.save_weights(checkpoint_path)
    # todo: double check checkpoint documentation

    # 4. SET TRAINING PARAMETERS
    reduce_lr = tf.keras.callbacks.ReduceLROnPlateau(monitor='loss', factor=0.4,
                                                     patience=15, min_lr=1e-9,
                                                     verbose=1, mode='min', min_delta=1)
    # The following outcommented rows to be included as an option during experiments:
    # lr_schedule = tf.keras.callbacks.LearningRateScheduler(
    #     lambda epoch: 1e-6 * 10 ** (epoch / 10))
    csv_logger = tf.keras.callbacks.CSVLogger(LOCAL_SAVING_DIR / LOCAL_LOG_FILE, append=True)
    cp_callback = tf.keras.callbacks.ModelCheckpoint(
        filepath=checkpoint_path,
        verbose=1,
        save_weights_only=True,
        save_freq=3 * BATCH_SIZE
    )

    # 5. TRAIN THE RNN
    Y_train.reshape(Y_train.shape[0], 1)
    dataset = tf.data.Dataset.from_tensor_slices((X_train, Y_train))
    dataset = dataset.batch(batch_size=BATCH_SIZE)
    prepared_dataset = dataset.shuffle(buffer_size=X_train.shape[1], reshuffle_each_iteration=True)

    history = model.fit(prepared_dataset,
                        epochs=EPOCHS,
                        shuffle=True,
                        callbacks=[reduce_lr, csv_logger, cp_callback]
                        )

    # The following outcommented rows to be included as an option during experiments:
    # plt.axis([1e-8, 1e-4, 0, 30])
    # plt.semilogx(history.history["lr"], history.history["loss"])
    # plt.show()
    # todo: Next steps:
    # normalise numbers?
    # within an input sequence, let's set up the last 'happiness' number to 1.
    # Then, convert the former ones to ratios with the previous number.
    # This way, we have all numbers in the vicinity of '1', and the NN will work better.
    # The maximum difference of ratio will be the sum of N.2 maximum pulses, that is 3+3=6.
    # At this point, numbers will not exhibit any more a high magnitude like thousands of units.

    return history
    # todo: add use of tensorboard


if __name__ == '__main__':
    pulses, effects = generate_effect_simulation(sample_plot=False,
                                                 max_pulse=False)
    # plt.plot(effects)
    all_x, all_y, X_train, X_test, Y_train, Y_test = prepare_training_set(pulses, effects)
    history = learn_with_rnn(X_train, X_test, Y_train, Y_test)
    plt.plot(history.epoch, history.history['loss'])
