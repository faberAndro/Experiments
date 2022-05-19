"""
A toy predictor for Happiness
"""

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from RNN_for_dumped_pulses.settings import DRIVE_DIR, LOG_FILE, CHECKPOINT_FILE

# ***** General parameters
N = 30000   # number of data points generated
K = 10  # parameter for the "speed" of exponential decay
np.random.seed(8)   # for repeatibility in pulses random generation
SHOW_INFLUX_GENERATION = False  # if TRUE, plots of impulses' decay are generated

# ***** parameters for animals' simualation
ANIMALS_LIST = ['dog', 'cat', 'bird', 'hamster', 'nothing', 'frog', 'spider', 'mosquito', 'wolf']
ANIMALS_PROBABILITY = [0.2, 0.2, 0.2, 0.1, 0.5, 0.1, 0.2, 0.3, 0.05]
ANIMALS_EFFECT = [2.5, 2.5, 2.0, 1.5, 0.0, -0.5, -2.5, -3.0, -3.0]
ANIMALS = dict(zip(ANIMALS_LIST, ANIMALS_EFFECT))

# ***** parameters for sun simulation
SUN_INTENSITY = [-3, -2, -1, 0, 1, 2, 3]
SUN_BASE_PROBABILITIES = [0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4]
PLOT_SIMULATION = True
DEMO_POINTS = 100

# ***** parameters for RNN
TRAIN_FRACTION = 0.8
WINDOW_SIZE = 64
BATCH_SIZE = 512
BATCH_SIZE_IN_TRAINING = 512
EPOCHS = 5       # 5 is for demo purpose. Set this parameter to 1000 for a real (long) run
RNN_OUTPUT_FACTOR_CORRECTION = 1000.0
INITIAL_LEARNING_RATE = 5*1e-5


def create_dumping_pulse(yp: int, kappa: int = K):
    y0 = abs(yp)
    alfa = (y0 - 0.1)/(1 - np.exp(-kappa))
    beta = y0 - alfa
    x = np.arange(0, kappa + 1)
    y = alfa * np.exp(-x) + beta
    y = y * np.sign(yp)
    return y


def compute_influx(pulses, k):
    n = len(pulses)
    influx = np.zeros(n)
    for i in range(n):
        final_index = min(i+k+1, n)
        extension = final_index - i
        id = create_dumping_pulse(pulses[i], k)[:extension]
        influx[i: final_index] += id
        if SHOW_INFLUX_GENERATION:
            to_plot = np.zeros(n)
            to_plot[i: final_index] += id
            plt.plot(to_plot[:200])
            plt.pause(0.5)
    if SHOW_INFLUX_GENERATION:
        plt.show()
    return influx


def generate_animal_influxes_simulation():
    animals_probability = ANIMALS_PROBABILITY/np.linalg.norm(ANIMALS_PROBABILITY, ord=1)
    animals_encountered = np.random.choice(a=ANIMALS_LIST, size=N, p=animals_probability)
    animals_pulses = np.asarray(list(map(lambda x: ANIMALS[x], animals_encountered)))
    animals_influx = compute_influx(pulses=animals_pulses, k=K)
    return animals_pulses, animals_influx


def generate_sun_influxes_simulation():
    # this function is different from the animal function, because ensure that there is not too much oscillation between
    # the level of sun in one day and in the following one (not too crazy weather but smooth enough to be real)
    sun_pulses = np.zeros(N)
    sun_pulses[0] = np.random.choice(a=SUN_INTENSITY, size=1)[0]
    for i in range(N):
        v = SUN_INTENSITY.index(sun_pulses[i - 1])
        c = len(SUN_BASE_PROBABILITIES)//2
        sun_probabilities = SUN_BASE_PROBABILITIES[c - v: c - v + c + 1]
        sun_probabilities_real = sun_probabilities / np.linalg.norm(sun_probabilities, ord=1)
        sun_pulses[i] = np.random.choice(a=SUN_INTENSITY, size=1, p=sun_probabilities_real)[0]
    sun_influx = compute_influx(pulses=sun_pulses, k=K)
    return sun_pulses, sun_influx


def combine_animals_and_sun(animals_pulses, animals_influx,
                            sun_pulses, sun_influx):
    # Creating configuration for pulses
    pulses_all = animals_pulses + sun_pulses
    influxes_all = animals_influx + sun_influx
    felicity = np.cumsum(influxes_all)
    # data = pd.DataFrame(columns=['animals', 'sun', 'happiness'])
    # data['animals'] = animals_encountered
    # data['sun'] = sun_pulses
    # data['pulses overall'] = pulses_all
    # data['happiness'] = felicity
    data = pd.DataFrame(columns=['animals', 'sun', 'happiness', 'pulses_all', 'influxes_all'],
                        data=np.vstack((animals_influx, sun_pulses, felicity, pulses_all, influxes_all)).transpose())
    return data


def plot_simulation(kind, pulses, influx):
    plt.figure()
    markerline, stemlines, baseline = plt.stem(pulses[:DEMO_POINTS],
                                               label=f'{kind}\' pulses',
                                               markerfmt='ro')
    plt.setp(stemlines, 'color', plt.getp(markerline, 'color'))
    plt.setp(stemlines, 'linestyle', 'dotted')
    plt.setp(markerline, markersize=2)
    plt.plot(influx[:DEMO_POINTS],
             label=f'{kind}\' influx',
             color='grey',
             linewidth=2)
    plt.legend()
    plt.grid(True)
    plt.show()


def learn_with_rnn(data):
    # todo: Next steps:
    # normalise numbers:
    # within an input sequence, let's set up the last 'happiness' number to 1.
    # Then, convert the former ones to ratios with the previous number.
    # This way, we have all numbers in the vicinity of '1', and the NN will work better.
    # The maximum difference of ratio will be the sum of N.2 maximum pulses, that is 3+3=6.
    # At this point, numbers will not exhibit any more a high magnitude like thousands of units.
    # Finally, it's important to check the WINDOW_SIZE depending on the maximum pulse duration
    # Set up callbacks and checkpoints
    import tensorflow as tf
    reduce_lr = tf.keras.callbacks.ReduceLROnPlateau(monitor='loss', factor=0.4,
                                                     patience=15, min_lr=1e-9,
                                                     verbose=1, mode='min', min_delta=1)
    # The following outcommented rows to be included as an option during experiments:
    # lr_schedule = tf.keras.callbacks.LearningRateScheduler(
    #     lambda epoch: 1e-6 * 10 ** (epoch / 10))
    csv_logger = tf.keras.callbacks.CSVLogger(DRIVE_DIR + LOG_FILE, append=True)
    checkpoint_path = DRIVE_DIR + CHECKPOINT_FILE
    cp_callback = tf.keras.callbacks.ModelCheckpoint(
        filepath=checkpoint_path,
        verbose=1,
        save_weights_only=True,
        save_freq=3 * BATCH_SIZE_IN_TRAINING)

    # Transform 'categorical columns' to 'numerical columns'
    data['animals'] = data['animals'].apply(lambda a: ANIMALS[a])

    # Generate numpy array for training:
    n_train = int(np.floor(N * TRAIN_FRACTION))
    training_data = data[:n_train]
    test_data = data[n_train:]
    true_number_of_data = n_train - WINDOW_SIZE + 1
    whole_batches_number = int(true_number_of_data // BATCH_SIZE)
    feature_columns = ['animals', 'sun']

    # Preparing RNN:
    model = tf.keras.models.Sequential(
        [
            tf.keras.layers.Dense(units=WINDOW_SIZE, input_shape=(WINDOW_SIZE, 2)),
            # tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(units=128, activation='swish', return_sequences=True)),
            tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(units=64, activation='swish')),
            tf.keras.layers.Dense(units=1, activation='swish'),
            tf.keras.layers.Lambda(lambda x: x * RNN_OUTPUT_FACTOR_CORRECTION)
        ]
    )
    optimizer = tf.keras.optimizers.Adam(lr=INITIAL_LEARNING_RATE)
    loss = tf.keras.losses.MeanAbsoluteError()
    metrics = ["mape"]
    model.compile(loss=loss,
                  optimizer=optimizer,
                  metrics=metrics)
    model.save(DRIVE_DIR + "saved_happiness_model")
    model.save_weights(checkpoint_path.format(epoch=0))

    # Train the RNN
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
    return history


if __name__ == '__main__':
    # Initialisation
    animals_pulses, animals_influx = generate_animal_influxes_simulation()
    sun_pulses, sun_influx = generate_sun_influxes_simulation()
    data = combine_animals_and_sun(animals_pulses, animals_influx,
                                   sun_pulses, sun_influx)
    # Plotting
    if PLOT_SIMULATION:
        plot_simulation(kind='animals', pulses=animals_pulses, influx=animals_influx)
        plot_simulation(kind='sun', pulses=sun_pulses, influx=sun_influx)
        print(np.corrcoef(data.influxes_all, data.happiness))
        print(data.happiness.mean())
