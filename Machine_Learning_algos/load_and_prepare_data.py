from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.utils import Bunch


def load_sample_dataset(dataset_name: str) -> Bunch:
    """

    :param dataset_name: can be one of the followings:
         'wine', 'iris', 'digits', 'breast cancer', 'diabetes', 'linnerud'
         For more details see the "settings.py" module
    :return: a sklearn Bunch dataset, completed with pandas datatypes.
    """
    dataset = {}
    if dataset_name == 'wine':
        dataset = datasets.load_wine(as_frame=True)
    elif dataset_name == 'iris':
        dataset = datasets.load_iris(as_frame=True)
    elif dataset_name == 'digits':
        dataset = datasets.load_digits(as_frame=True)
    elif dataset_name == 'breast cancer':
        dataset = datasets.load_breast_cancer(as_frame=True)
    elif dataset_name == 'diabetes':
        dataset = datasets.load_diabetes(as_frame=True)
    elif dataset_name == 'linnerud':
        dataset = datasets.load_linnerud(as_frame=True)
    return dataset


def prepare_trainig_data(dataset, test_size: float = 0.3) -> tuple:
    training_data = train_test_split(dataset.data,
                                     dataset.target,
                                     test_size=test_size,
                                     random_state=0)
    return training_data
