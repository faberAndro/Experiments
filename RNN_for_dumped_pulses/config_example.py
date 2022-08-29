# ***** parameters for pulses' generation
N = 50000                   # number of pulses generated (data points)
MPH = 10                    # max pulse height
SL = 10                     # sequence length: number of time steps passed each time to the RNN
RANDOM_LEN = True           # sequences are created with random length between SL and 2*SL
USE_NEGATIVE_PULSES = False

# ***** parameters for RNN
TRAIN_FRACTION = 0.8
EPOCHS = 20         # 5 is for demo purpose. Set this parameter to 1000 for a real (long) run
BATCH_SIZE = 256
INITIAL_LEARNING_RATE = 5 * 1e-5

# ***** plot parameters
MAX_PULSE_TO_PLOT = 200
PLOT_EFFECTS = False
