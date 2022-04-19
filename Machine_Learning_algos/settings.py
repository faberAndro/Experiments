import pathlib

WORKING_DIR = pathlib.Path(__file__).parent.resolve()
TREE_GRAPHS_FOLDER = WORKING_DIR / 'dtree_graphs'

COMPLETE_DATASET_NAMES = ['wine', 'iris', 'digits', 'breast cancer', 'diabetes', 'linnerud']
CLASSIFICATION_TYPE_DATASETS = ['wine', 'iris', 'digits', 'breast cancer']
MULTI_OUPUT_REGRESSION_TYPE_DATASETS = ['linnerud']
REGRESSION_TYPE_DATASETS = ['diabetes']
