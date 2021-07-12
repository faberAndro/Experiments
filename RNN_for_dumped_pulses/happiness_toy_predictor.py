# -*- coding: utf-8 -*-
"""
A toy predictor for Happiness
This version in intended for use in GitHub
"""

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import tensorflow as tf

# PARAMETERS
show_influx_generation = False
verbose = False
np.random.seed(8)  

n = 30000
k = 10
TRAIN_FRACTION = 0.8
window_size = 64
batch_size = 512
batch_size_in_training = 512
EPOCHS = 1000
RNN_OUTPUT_FACTOR_CORRECTION = 1000.0
INITIAL_LEARNING_RATE = 5*1e-5


def dumping_pulse(yp: int, kappa: int):
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
        id = dumping_pulse(pulses[i], k)[:extension]
        influx[i: final_index] += id
        if show_influx_generation:
            to_plot = np.zeros(n)
            to_plot[i: final_index] += id
            plt.plot(to_plot[:200])
            plt.pause(0.5)
    if show_influx_generation:
        plt.show()
    return influx


animals_list = ['dog', 'cat', 'bird', 'hamster', 'nothing', 'frog', 'spider', 'mosquito', 'wolf']
animals = dict(zip(animals_list,
                    [2.5, 2.5, 2.0, 1.5, 0.0, -0.5, -2.5, -3.0, -3.0]))
animals_probability = [0.2, 0.2, 0.2, 0.1, 0.5, 0.1, 0.2, 0.3, 0.05]
animals_probability = animals_probability/np.linalg.norm(animals_probability, ord=1)
animals_encountered = np.random.choice(a=animals_list, size=n, p=animals_probability)
animals_pulses = list(map(lambda x: animals[x], animals_encountered))
animals_influx = compute_influx(pulses=animals_pulses, k=k)

sun_intensity = [-3, -2, -1, 0, 1, 2, 3]
sun_base_probabilities = [0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4]
sun_pulses = np.zeros(n)
sun_pulses[0] = np.random.choice(a=sun_intensity, size=1)[0]
for i in range(n):
    v = sun_intensity.index(sun_pulses[i-1])
    sun_probabilities = sun_base_probabilities[6-v: 6-v+7]
    sun_probabilities_real = sun_probabilities / np.linalg.norm(sun_probabilities, ord=1)
    sun_pulses[i] = np.random.choice(a=sun_intensity, size=1, p=sun_probabilities_real)[0]
    if verbose:
        print(v, sun_probabilities)
sun_influx = compute_influx(pulses=sun_pulses, k=k)

pulses_all = animals_pulses + sun_pulses
influxes_all = animals_influx + sun_influx
felicity = np.cumsum(influxes_all)
data = pd.DataFrame(columns=['animals', 'sun', 'happiness'])
data['animals'] = animals_encountered
data['sun'] = sun_pulses
data['pulses overall'] = pulses_all
data['happiness'] = felicity

plt.plot(animals_influx, label='animals (influxes)')
plt.plot(sun_influx, label='sun (influxes)')
plt.plot(influxes_all, label='influx (overall)')
plt.plot(felicity, label='happiness')
plt.legend()
plt.grid(True)
plt.show()
print(np.corrcoef(influxes_all, felicity))
print(felicity.mean())

# SET UP CALLBACKS AND CHECKPOINTS
reduce_lr = tf.keras.callbacks.ReduceLROnPlateau(monitor='loss', factor=0.4,
                                                 patience=15, min_lr=1e-9,
                                                 verbose=1, mode='min', min_delta=1)
# lr_schedule = tf.keras.callbacks.LearningRateScheduler(
#     lambda epoch: 1e-6 * 10 ** (epoch / 10))
drive_dir = "/content/drive/My Drive/Colab_files/happiness/"
csv_logger = tf.keras.callbacks.CSVLogger(drive_dir + "model_history_log.csv", append=True)

checkpoint_path = drive_dir + "training_2/cp-{epoch:04d}.ckpt"
cp_callback = tf.keras.callbacks.ModelCheckpoint(
    filepath=checkpoint_path, 
    verbose=1, 
    save_weights_only=True,
    save_freq=3*batch_size_in_training)

# transform 'categorical columns' to 'numerical columns'
data['animals'] = data['animals'].apply(lambda a: animals[a])
# generate numpy array for training:
n_train = int(np.floor(n * TRAIN_FRACTION))
training_data = data[:n_train]
test_data = data[n_train:]
true_number_of_data = n_train - window_size + 1
whole_batches_number = int(true_number_of_data // batch_size)
feature_columns = ['animals', 'sun']

# preparing RNN:
model = tf.keras.models.Sequential(
    [
        tf.keras.layers.Dense(units=window_size, input_shape=(window_size, 2)),
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
model.save(drive_dir + "saved_happiness_model")
model.save_weights(checkpoint_path.format(epoch=0))

# TRAIN THE RNN
batch_of_features = np.asarray([training_data.iloc[i: i + window_size][feature_columns].to_numpy() for i in range(true_number_of_data)])
batch_of_labels = training_data['happiness'].iloc[window_size - 1:].to_numpy()
history = model.fit(x=batch_of_features,
                    y=batch_of_labels,
                    batch_size=batch_size_in_training,
                    epochs=EPOCHS,
                    shuffle=True,
                    callbacks=[reduce_lr, csv_logger, cp_callback]
                    )
# plt.axis([1e-8, 1e-4, 0, 30])
# plt.semilogx(history.history["lr"], history.history["loss"])
# plt.show()

"""Next improvement:
normalise numbers:
within an input sequence, let's set up the last 'happiness' number to 1.
Then, convert the former ones to ratios with the previous number.
This way, we have all numbers in the vicinity of '1', and the NN will work better.
The maximum difference of ratio will be the sum of N.2 maximum pulses, that is 3+3=6.
At this point, numbers will not exhibit any more a high magnitude like thousands of units. 
Finally, it's important to check the window_size depending on the maximum pulse duration 
"""
