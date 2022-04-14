import graphviz
import numpy as np
from sklearn import datasets, svm, tree
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB, ComplementNB
from sklearn.utils import Bunch

DATASET_NAMES = ['wine', 'iris', 'digits', 'diabetes', 'breast cancer', 'linnerud']


def load_sample_dataset(dataset_name: str) -> Bunch:
    dataset = {}
    if dataset_name == 'wine':
        dataset = datasets.load_wine(as_frame=True)
    elif dataset_name == 'iris':
        dataset = datasets.load_iris(as_frame=True)
    elif dataset_name == 'digits':
        dataset = datasets.load_digits(as_frame=True)
    elif dataset_name == 'brest cancer':
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


def use_naive_bayes(training_data: tuple) -> dict:
    X_train, X_test, y_train, y_test = training_data
    naive_bayes_models = [GaussianNB(), MultinomialNB(), BernoulliNB(), ComplementNB()]
    scores = {}
    for algo in naive_bayes_models:
        algo_type = str(algo)[:-2]
        print(f'using {algo_type}', end=': ')
        naive_model = algo
        naive_model.fit(X_train, y_train)
        y_pred = naive_model.predict(X_test)
        print(f'mislabeled points: {np.array((y_test != y_pred)).sum()} out of {X_test.shape[0]}')
        scores.update(
            {algo_type: naive_model.score(X_test, y_test)}
        )
    return scores


def use_decision_tree(training_data: tuple,
                      raw_data: Bunch,
                      tree_graph_filename: str = 'DtreeGraph',
                      plot_and_save: bool = True) -> float:

    output_filename = './dtree_graphs/' + tree_graph_filename
    X_train, X_test, y_train, y_test = training_data
    clf = tree.DecisionTreeClassifier(criterion='gini',
                                      max_depth=3)
    clf = clf.fit(X_train, y_train)
    score = clf.score(X_test, y_test)
    print('Tree score:', score)

    # plotting and saving the tree structure and info
    if plot_and_save:
        tree.plot_tree(clf)     # this if you want just a simple plot without saving it to file.
        dot_data = tree.export_graphviz(clf,
                                        out_file=None,
                                        feature_names=training_data[0].columns,
                                        class_names=raw_data.target_names,
                                        filled=True,
                                        rounded=True,
                                        special_characters=True,
                                        leaves_parallel=True,
                                        impurity=True)
        graph = graphviz.Source(dot_data)
        graph.render(output_filename)
    return score


def use_support_vector_machine(training_data: tuple) -> float:

    X_train, X_test, y_train, y_test = training_data
    clf = svm.LinearSVC(    # this works better than the other two.
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
        max_iter=2000
    )
    clf.fit(X_train, y_train)
    score = clf.score(X_test, y_test)
    print(score)
    return score


if __name__ == '__main__':
    results_list = []
    for sample_dataset_name in DATASET_NAMES[:-1]:
        use_case_dataset = load_sample_dataset(sample_dataset_name)
        use_case_training_data = prepare_trainig_data(use_case_dataset)
        print(f'Considering {sample_dataset_name}')
        naive_bayes_result = use_naive_bayes(training_data=use_case_training_data)
        dtree_result = use_decision_tree(training_data=use_case_training_data,
                                         raw_data=use_case_dataset,
                                         plot_and_save=False)
        svm_result = use_support_vector_machine(training_data=use_case_training_data)
        results_list.append(
            dict(
                {
                    'dataset': sample_dataset_name,
                    'svm': svm_result,
                    'decision tree': dtree_result
                },
                **naive_bayes_result
            )
        )
