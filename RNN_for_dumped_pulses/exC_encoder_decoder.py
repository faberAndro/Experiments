from tensorflow.keras.preprocessing.text import one_hot
from tensorflow import keras
from tensorflow.keras import layers

example = 'I want to be a good example'
for vocab_size in range(10, 100, 10):
    print('Vocab size:', vocab_size, end=' ')
    oh = one_hot(example, vocab_size)
    print(oh)

# -------------------------------------------------------------

encoder_vocab = 1000
decoder_vocab = 2000

encoder_input = layers.Input(shape=(None,))
encoder_embedded = layers.Embedding(input_dim=encoder_vocab, output_dim=64)(encoder_input)
# Return states in addition to output
encoder_output, state_h, state_c = layers.LSTM(64, return_state=True, name="encoder")(encoder_embedded)
encoder_state = [state_h, state_c]

decoder_input = layers.Input(shape=(None,))
decoder_embedded = layers.Embedding(input_dim=decoder_vocab, output_dim=64)(decoder_input)
# Pass the 2 states to a new LSTM layer, as initial state
decoder_output = layers.LSTM(64, name="decoder")(decoder_embedded, initial_state=encoder_state)
rnn_output = layers.Dense(10)(decoder_output)

model = keras.Model([encoder_input, decoder_input], rnn_output)
model.summary()
