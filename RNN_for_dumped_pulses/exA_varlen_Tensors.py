"""
A sample RNN to learn superposition of pulses that dump over
"""
import os
from datetime import datetime
from RNN_for_dumped_pulses.settings import WORKING_DIR, LOG_FILENAME, CHECKPOINT_SUBFOLDER, LOCAL_CHECKPOINT_FILENAME

INITIAL_LEARNING_RATE = 0.01
EPOCHS = 5


def convert_vl_dataset_to_tf_dataset(x_train, y_train):
    from tensorflow import data, TensorSpec, as_dtype
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
    from keras import layers, models, callbacks, losses, optimizers
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
    from keras import layers, models
    model = models.Sequential(
        [
            layers.LSTM(units=64, activation='tanh', input_shape=(None, 1)),
            layers.Dense(units=1)  # try also "swish". This neuron has no activation f.
        ]
    )
    model.compile()
    history = model.fit(x=x_train, y=y_train)
    return history
