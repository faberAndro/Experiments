"""
A sample RNN to learn superposition of pulses that dump over
"""

import numpy as np
from matplotlib import pyplot as plt
from RNN_for_dumped_pulses.settings import DRIVE_DIR, LOG_FILE, CHECKPOINT_FILE

# np.random.seed(8)   # for repeatibility in pulses random generation

# ***** parameters for pulses' generation
N = 300   # number of pulses generated
MPH = 10  # max pulse height
MAX_PULSE_TO_PLOT = 200

# ***** parameters for RNN
TRAIN_FRACTION = 0.8
WINDOW_SIZE = 64
BATCH_SIZE = 512
BATCH_SIZE_IN_TRAINING = 512
EPOCHS = 5       # 5 is for demo purpose. Set this parameter to 1000 for a real (long) run
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
    influx = np.zeros(n + MPH*2)
    for i in range(n):
        pulse_points = create_dumping_pulse(pulse_heights[i], **kwargs)
        influx[i: i + len(pulse_points)] += pulse_points
        if sample_plot and i <= MAX_PULSE_TO_PLOT:
            x_stream = np.zeros(n + MPH*2)
            x_stream[i: i + len(pulse_points)] = pulse_points
            plt.plot(x_stream)
            plt.show()
    return influx


def generate_influxes_simulation(**kwargs):
    """

    :param kwargs: max_pulse, sample_plot
    :return:
    """
    pulses_train = np.random.randint(MPH + 1, size=N)
    influx = compute_influx(pulses_train, **kwargs)
    return influx


def learn_with_rnn(pulses, influxes):
    # Animal pulses are input. Animal influx is output (y hat)
    import tensorflow as tf
    from sklearn.model_selection import train_test_split

    # 1. PREPARE TRAINING DATA:
    training_data, X_test, Y_train, Y_test = train_test_split(
        pulses, influxes, test_size=1-TRAIN_FRACTION, random_state=0)
    n_train = int(np.floor(N * TRAIN_FRACTION))
    true_number_of_data = n_train - WINDOW_SIZE + 1
    feature_columns = ['animals', 'sun']

    # 2. BUILD RNN ARCHITECTURE:
    model = tf.keras.models.Sequential(
        [
            tf.keras.layers.Dense(units=WINDOW_SIZE, input_shape=(WINDOW_SIZE, 2)),
            # it doesn't have sense to make the network bidirectional here: type to be changed
            tf.keras.layers.LSTM(units=64, activation='swish'),
            tf.keras.layers.Dense(units=1, activation='swish'),
            tf.keras.layers.Lambda(lambda x: x * RNN_OUTPUT_FACTOR_CORRECTION)
        ]
    )
    optimizer = tf.keras.optimizers.Adam(lr=INITIAL_LEARNING_RATE)
    loss = tf.keras.losses.MeanAbsoluteError()
    metrics = ["mape"]  # maybe metric to be changed with a better one
    model.compile(loss=loss,
                  optimizer=optimizer,
                  metrics=metrics)

    # 3. SET DATA SAVE & CHECKPOINTS
    model.save(DRIVE_DIR + "saved_happiness_model")
    checkpoint_path = DRIVE_DIR + CHECKPOINT_FILE
    model.save_weights(checkpoint_path.format(epoch=0))

    # 4. SET TRAINING PARAMETERS
    reduce_lr = tf.keras.callbacks.ReduceLROnPlateau(monitor='loss', factor=0.4,
                                                     patience=15, min_lr=1e-9,
                                                     verbose=1, mode='min', min_delta=1)
    # The following outcommented rows to be included as an option during experiments:
    # lr_schedule = tf.keras.callbacks.LearningRateScheduler(
    #     lambda epoch: 1e-6 * 10 ** (epoch / 10))
    csv_logger = tf.keras.callbacks.CSVLogger(DRIVE_DIR + LOG_FILE, append=True)
    cp_callback = tf.keras.callbacks.ModelCheckpoint(
        filepath=checkpoint_path,
        verbose=1,
        save_weights_only=True,
        save_freq=3 * BATCH_SIZE_IN_TRAINING
    )

    # 5. TRAIN THE RNN
    batch_of_features = np.asarray([training_data.iloc[i: i + WINDOW_SIZE][feature_columns].to_numpy()
                                    for i in range(true_number_of_data)])
    batch_of_labels = training_data['happiness'].iloc[WINDOW_SIZE - 1:].to_numpy()
    history = model.fit(x=batch_of_features,
                        y=batch_of_labels,
                        batch_size=BATCH_SIZE_IN_TRAINING,
                        epochs=EPOCHS,
                        shuffle=True,
                        callbacks=[reduce_lr, csv_logger, cp_callback]
                        )

    # The following outcommented rows to be included as an option during experiments:
    # plt.axis([1e-8, 1e-4, 0, 30])
    # plt.semilogx(history.history["lr"], history.history["loss"])
    # plt.show()

    # todo: Next steps:
    # normalise numbers:
    # within an input sequence, let's set up the last 'happiness' number to 1.
    # Then, convert the former ones to ratios with the previous number.
    # This way, we have all numbers in the vicinity of '1', and the NN will work better.
    # The maximum difference of ratio will be the sum of N.2 maximum pulses, that is 3+3=6.
    # At this point, numbers will not exhibit any more a high magnitude like thousands of units.
    # Finally, it's important to check the WINDOW_SIZE depending on the maximum pulse duration
    # Set up callbacks and checkpoints

    return history


if __name__ == '__main__':
    # Initialisation
    influxes = generate_influxes_simulation(sample_plot=True,
                                            max_pulse=False)
    plt.plot(influxes)
    # Plotting
    if False:
        plot_simulation(kind='animals', pulses=animals_pulses, influx=animals_influx)
        plot_simulation(kind='sun', pulses=sun_pulses, influx=sun_influx)
        print(np.corrcoef(data.influxes_all, data.happiness))
        print(data.happiness.mean())
