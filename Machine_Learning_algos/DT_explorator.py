import os
import pathlib
import pprint

import graphviz
from matplotlib import pyplot as plt
from sklearn import tree

from Machine_Learning_algos.load_and_prepare_data import load_sample_dataset, prepare_trainig_data
from Machine_Learning_algos.settings import WORKING_DIR, TREE_GRAPHS_FOLDER

VISUALISE_DATA = False
SAMPLE_DATASET_NAME = 'wine'
DT_GRAPH_FILENAME = 'dt_exploration_test'

# LOADING DATASET
os.chdir(WORKING_DIR)
use_case_dataset = load_sample_dataset(SAMPLE_DATASET_NAME)
use_case_training_data = prepare_trainig_data(use_case_dataset)
X_train, X_test, y_train, y_test = use_case_training_data


def export_graph(filename: str,
                 generated_tree: tree.DecisionTreeClassifier,
                 feature_names: tuple, target_names: tuple
                 ) -> pathlib.Path:
    dot_data = tree.export_graphviz(generated_tree,
                                    out_file=None,
                                    feature_names=feature_names,
                                    class_names=target_names,
                                    filled=True,
                                    rounded=True,
                                    special_characters=True,
                                    rotate=True)
    graph = graphviz.Source(dot_data)
    output_filepath = TREE_GRAPHS_FOLDER / filename
    graph.render(str(output_filepath))
    # alternative ways of plotting:
    # graph = pydotplus.graph_from_dot_data(dot_data)
    # graph.write_png('test_DT3.png')
    return output_filepath / '.pdf'


def explore_changes_in_max_depth(export_filename: str = None):
    # EXPLORING CHANGES IN max_depth:
    _clf = None
    param = list(range(1, 30))
    results = {}
    for p in param:
        _clf = tree.DecisionTreeClassifier(max_depth=p)
        _clf.fit(X_train, y_train, sample_weight=None)
        score = _clf.score(X_test, y_test)
        real_depth = _clf.get_depth()
        results[p] = {'score': score, 'effective depth': real_depth}
    plt.figure()
    plt.plot(param, [result['score'] for result in results.values()], label='score vs. max theoretical depth')
    plt.plot(param, [result['effective depth'] for result in results.values()],
             label='real depth vs. max theoretical depth')
    pprint.pprint(results)
    plt.legend()
    plt.show()
    if export_filename:
        export_graph(export_filename, _clf,
                     use_case_dataset.feature_names, use_case_dataset.target_names)


def explore_changes_in_min_samples_split(export_filename: str = None):
    _clf = None
    param = list(range(2, len(X_train)))
    results = {}
    for p in param:
        _clf = tree.DecisionTreeClassifier(min_samples_split=p)
        _clf.fit(X_train, y_train)
        score = _clf.score(X_test, y_test)
        features_seen = _clf.n_features_in_
        leaves = _clf.get_n_leaves()
        results[p] = {'score': score, 'features': features_seen, 'leaves': leaves}
    plt.figure()
    plt.plot(param, [result['score'] for result in results.values()], label='score')
    plt.plot(param, [result['features'] for result in results.values()], label='features used')
    plt.plot(param, [result['leaves'] for result in results.values()], label='number of leaves')
    plt.xlabel('min. samples to split')
    pprint.pprint(results)
    plt.legend()
    plt.show()
    if export_filename:
        export_graph(export_filename, _clf,
                     use_case_dataset.feature_names, use_case_dataset.target_names)


def explore_changes_in_min_samples_for_leaves(export_filename: str = None):
    # EXPLORING CHANGES IN max_depth:
    _clf = None
    param = list(range(1, len(X_train)))
    results = {}
    for p in param:
        _clf = tree.DecisionTreeClassifier(min_samples_leaf=p)
        _clf.fit(X_train, y_train)
        score = _clf.score(X_test, y_test)
        leaves = _clf.get_n_leaves()
        results[p] = {'score': score, 'leaves': leaves}
    plt.figure()
    plt.plot(param, [result['score'] for result in results.values()], label='score')
    plt.plot(param, [result['leaves'] for result in results.values()], label='number of leaves')
    plt.xlabel('min. samples for terminal leaves')
    pprint.pprint(results)
    plt.legend()
    plt.show()
    if export_filename:
        export_graph(export_filename, _clf,
                     use_case_dataset.feature_names, use_case_dataset.target_names)


if __name__ == '__main__':
    explore_changes_in_max_depth()
    explore_changes_in_min_samples_split('sample_test_for_DT_exploration')
    explore_changes_in_min_samples_for_leaves()
    # todo: explore changes in max_leaf_node, max_features, impurity, min_weight
