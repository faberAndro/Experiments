from Machine_Learning_algos import load_and_prepare_data as lsd
from sklearn import tree
import graphviz
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import pprint
import pathlib
import os

WORKING_DIR = pathlib.Path(__file__).parent.resolve()
os.chdir(WORKING_DIR)
visualise_data = False

# LOADING DATASET
X_train, X_test, y_train, y_test, df = lsd.load_data(which='wine')


def explore_changes_in_max_depth():
    # EXPLORING CHANGES IN max_depth:
    param = list(range(1, 30))
    results = {}
    for p in param:
        _clf = tree.DecisionTreeClassifier(max_depth=p)
        _clf.fit(X_train, y_train, sample_weight=None)

        score = _clf.score(X_test, y_test)
        real_depth = _clf.get_depth()

        results[p] = {'score': score, 'effective depth': real_depth}

    plt.plot(param, [result['score'] for result in results.values()], label='score vs. max theoretical depth')
    plt.plot(param, [result['effective depth'] for result in results.values()], label='real depth vs. max theoretical depth')
    pprint.pprint(results)
    plt.legend()
    plt.show()


def explore_changes_in_min_samples_split():
    param = list(range(2, len(X_train)))
    results = {}
    for p in param:
        _clf = tree.DecisionTreeClassifier(min_samples_split=p)
        _clf.fit(X_train, y_train)
        score = _clf.score(X_test, y_test)
        features_seen = _clf.n_features_in_
        leaves = _clf.get_n_leaves()
        results[p] = {'score': score, 'features': features_seen, 'leaves': leaves}
    plt.plot(param, [result['score'] for result in results.values()], label='score')
    plt.plot(param, [result['features'] for result in results.values()], label='features used')
    plt.plot(param, [result['leaves'] for result in results.values()], label='number of leaves')
    plt.xlabel('min. samples to split')
    pprint.pprint(results)
    plt.legend()
    plt.show()


def explore_changes_in_min_samples_for_leaves():
    # EXPLORING CHANGES IN max_depth:
    param = list(range(1, len(X_train)))
    results = {}
    for p in param:
        _clf = tree.DecisionTreeClassifier(min_samples_leaf=p)
        _clf.fit(X_train, y_train)
        score = _clf.score(X_test, y_test)
        leaves = _clf.get_n_leaves()
        results[p] = {'score': score, 'leaves': leaves}
    plt.plot(param, [result['score'] for result in results.values()], label='score')
    plt.plot(param, [result['leaves'] for result in results.values()], label='number of leaves')
    plt.xlabel('min. samples for terminal leaves')
    pprint.pprint(results)
    plt.legend()
    plt.show()


if __name__ == '__main__':
    explore_changes_in_max_depth()
    explore_changes_in_min_samples_split()
    explore_changes_in_min_samples_for_leaves()
    # todo: explore changes in max_leaf_node, max_features, impurity, min_weight

if visualise_data:

    clf = tree.DecisionTreeClassifier(min_samples_leaf=4)
    clf.fit(X_train, y_train)

    # SIMPLE PLOT
    tree.plot_tree(clf)
    # SIMPLE EXPORT
    dot_data = tree.export_graphviz(clf, out_file=None)
    graph = graphviz.Source(dot_data)
    graph.render("test_DT")
    # IMPROVED EXPORT
    dot_data = tree.export_graphviz(clf,
                                    out_file=None,
                                    feature_names=df.columns[:-1],
                                    class_names=df.columns[-1],
                                    filled=True,
                                    rounded=True,
                                    special_characters=True,
                                    rotate=True)
    graph = graphviz.Source(dot_data)
    graph.render("test_DT_2")

    # graph = pydotplus.graph_from_dot_data(dot_data)
    # graph.write_png('test_DT3.png')
