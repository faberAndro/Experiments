import pandas as pd
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.utils import Bunch

global dataset


def load_data(which: str, test_size: float = 0.3) -> tuple:
    """

    :param which: could be: iris, diabetes, digits, linnerud, wine, breast_cancer
    :param test_size: the fraction of the test dataset to prepare
    :return: X_train, X_test, y_train, y_test, summary dataframe
    """

    # VISUALISING DATA IN A DATAFRAME
    # dataset = Bunch()
    loading_string = f'global dataset; dataset = datasets.load_{which}()'
    exec(loading_string)
    df = pd.DataFrame(data=dataset.data, columns=dataset.feature_names)
    if which != 'linnerud':
        df = df.assign(target=dataset.target)
    else:
        df = df.assign(target=tuple(dataset.target))
    # PREPARING DATA
    X, y = dataset.data, dataset.target
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=0)
    return X_train, X_test, y_train, y_test, df


if __name__ == '__main__':
    test = load_data(which='iris',
                     test_size=0.2
                     )
