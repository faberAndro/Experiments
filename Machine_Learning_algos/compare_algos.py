import graphviz
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from sklearn import datasets
from sklearn.model_selection import train_test_split

from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB, ComplementNB
from sklearn import tree
from sklearn import svm


DATASET_NAMES = ['wine', 'iris']


def visualise_sample_dataset(dataset_name: str):
    dataset = {}
    if dataset_name == 'wine':
        dataset = datasets.load_wine(as_frame=True)
    elif dataset_name == 'iris':
        dataset = datasets.load_iris(as_frame=True)
    return dataset


def prepare_trainig_data(dataset, test_size: float = 0.3):
    training_data = train_test_split(dataset.data,
                                     dataset.target,
                                     test_size=test_size,
                                     random_state=0)
    return training_data


def use_naive_bayes(training_data: tuple) -> dict:
    X_train, X_test, y_train, y_test = training_data
    naive_bayes_models = [GaussianNB(), MultinomialNB(), BernoulliNB(), ComplementNB()]
    scores = {}
    for algo in naive_bayes_models:
        print(f'using {str(algo)[:-2]}', end=': ')
        naive_model = algo
        naive_model.fit(X_train, y_train)
        y_pred = naive_model.predict(X_test)
        print(f'mislabeled points: {np.array((y_test != y_pred)).sum()} out of {X_test.shape[0]}')
        scores.update(
            {algo: naive_model.score(X_test, y_test)}
        )
    return scores


def use_decision_tree(train_test_data: tuple):
    output_filename = 'wine'
    X_train, X_test, y_train, y_test = train_test_data

    clf = tree.DecisionTreeClassifier(criterion='gini', max_depth=3)
    clf = clf.fit(X_train, y_train)
    prediction = clf.predict(X_test)
    score = clf.score(X_test, y_test)
    print('score', score)

    p = pd.DataFrame(data=y_test, columns=['ground truth'])
    p = p.assign(prediction=prediction)
    p_score = np.array(p['ground truth'] == p['prediction']).sum()/len(p)
    print('p score', p_score)

    # plotting the tree
    tree.plot_tree(clf)
    dot_data = tree.export_graphviz(clf,
                                    out_file=None)
    graph = graphviz.Source(dot_data)
    graph.render(f"{output_filename}.txt")

    dot_data = tree.export_graphviz(clf,
                                    out_file=None,
                                    feature_names=dataset.feature_names,
                                    class_names=dataset.target_names,
                                    filled=True,
                                    rounded=True,
                                    special_characters=True)
    graph = graphviz.Source(dot_data)
    graph.render(output_filename)


def use_svm(c):
    clf = svm.SVC(C=c)
    clf.fit(X_train, y_train)
    clf.predict(X_train)
    return clf.score(X_test, y_test)


def use_support_vector_machines():
    results = dict()
    for c in range(1, 10):
        results[c/10] = use_svm(c=c/10)
    for c in range(1, 10):
        results[c] = use_svm(c=c)

    plt.xscale('log')
    plt.plot(list(results.keys()), list(results.values()))

    sv = clf.support_vectors_
    svi = clf.support_
    svc = clf.n_support_

    clf = svm.SVC(
            C=1.0,
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


    clf = svm.LinearSVC(    # this works better then the other two.
        C=1.0,
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
    clf.fit(X_train, y_train)
    clf.predict(X_train)
    clf.score(X_test, y_test)

    clf = svm.NuSVC(nu=0.5,
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
                    random_state=None)
    clf.fit(X_train, y_train)
    clf.predict(X_train)
    clf.score(X_test, y_test)


if __name__ == '__main__':
    use_case_dataset = visualise_sample_dataset('wine')
    use_case_training_data = prepare_trainig_data(use_case_dataset)
    ml_result = use_naive_bayes(training_data=use_case_training_data)
