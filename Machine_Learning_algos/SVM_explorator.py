from matplotlib import pyplot as plt
from sklearn import svm
from sklearn.datasets import make_blobs
from Machine_Learning_algos.load_and_prepare_data import load_sample_dataset, prepare_trainig_data
import numpy as np

SAMPLE_DATASET_NAME = 'iris'

use_case_dataset = load_sample_dataset(SAMPLE_DATASET_NAME)
use_case_training_data = prepare_trainig_data(use_case_dataset)
X_train, X_test, y_train, y_test = use_case_training_data


def use_simple_svc(c: float = 1.0):
    _clf = svm.SVC(
            C=c,
            kernel='rbf',
            degree=3,
            gamma='scale',
            coef0=0.0,
            shrinking=True,
            probability=False,
            tol=0.001,
            cache_size=200,
            class_weight=None,
            verbose=False,
            max_iter=- 1,
            decision_function_shape='ovr',
            break_ties=False,
            random_state=None
            )
    return _clf


def use_linear_svc(c: float = 1.0):
    _clf = svm.LinearSVC(    # this works better than the other two.
        C=c,
        penalty='l2',
        loss='squared_hinge',
        dual=True,
        tol=0.0001,
        multi_class='ovr',
        fit_intercept=True,
        intercept_scaling=1,
        class_weight=None,
        verbose=0,
        random_state=None,
        max_iter=1000
    )
    return _clf


def use_nusvc():
    _clf = svm.NuSVC(
        nu=0.5,
        kernel='rbf',
        degree=3,
        gamma='scale',
        coef0=0.0,
        shrinking=True,
        probability=False,
        tol=0.001,
        cache_size=200,
        class_weight=None,
        verbose=False,
        max_iter=- 1,
        decision_function_shape='ovr',
        break_ties=False,
        random_state=None
    )
    return _clf


if __name__ == '__main__':

    method = linear_svc

    # MAKE DEMO BLOBS
    X, y_true = make_blobs(n_samples=500, centers=2, cluster_std=0.7, random_state=0)
    plt.scatter(X[:, 0], X[:, 1], s=20)

    # PLOTTING SVM SCORES VS. DIFFERENT VALUES OF 'C':
    results = dict()
    # varying the penalty param between 0 and 1, then between 1 and 10
    penalty_params = np.append(np.arange(0.1, 1, 0.1), np.arange(1, 11, 1))
    for p in penalty_params:
        clf = method(c=p)
        clf.fit(X_train, y_train)
        score = clf.score(X_test, y_test)
        # return info on support vectors: to be better developed
        if method == use_simple_svc:
            sv = clf.support_vectors_
            svi = clf.support_
            svc = clf.n_support_
        #
        results.update({p: score})
    # plotting
    plt.figure()
    plt.xlabel('C')
    plt.ylabel('score')
    plt.xscale('log')
    plt.title('Score vs C in SVM')
    plt.plot(list(results.keys()), list(results.values()))
    plt.show()
