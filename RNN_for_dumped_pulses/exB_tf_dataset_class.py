import numpy as np
from tensorflow import data, TensorSpec, as_dtype


def explore_ds(ds):
    return next(iter(ds))


np.random.seed(1)
sample_training_data = np.random.randint(10, size=(6, 5))
test_ds = data.Dataset.from_tensor_slices(sample_training_data)
test_ds = test_ds.map(lambda x: x+1)
test_ds_iter = iter(test_ds)
