import pandas as pd
from sklearn import datasets
from sklearn.model_selection import train_test_split
import graphviz
from matplotlib import pyplot as plt
naive_bayes_models = ['GaussianNB', 'MultinomialNB', 'BernoulliNB', 'ComplementNB']
exec(f'from sklearn.naive_bayes import {",".join(naive_bayes_models)}')
from sklearn import tree
from sklearn import svm

# VISUALISING DATA IN A DATAFRAME
wines = datasets.load_wine()
# from sklearn.datasets import load_iris
# X, y = load_iris(return_X_y=True)
dataset = wines
df = pd.DataFrame(data=dataset.data, columns=dataset.feature_names)
df = df.assign(target=dataset.target)

# PREPARING DATA
X, y = dataset.data, dataset.target
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

# USING NAIVE BAYES
for algo in naive_bayes_models:
    print(f'using {algo}', end=': ')
    exec(f'naive_model = {algo}()')
    naive_model.fit(X_train, y_train)
    y_pred = naive_model.predict(X_test)
    print(f'mislabeled points: {(y_test != y_pred).sum()} out of {X_test.shape[0]}')

# USING DECISION TREES
clf = tree.DecisionTreeClassifier(criterion='gini',
                                  max_depth=3)
clf = clf.fit(X_train, y_train)
prediction = clf.predict(X_test)
score = clf.score(X_test, y_test)
p = pd.DataFrame(data=y_test, columns=['ground truth'])
p = p.assign(prediction=prediction)
p_score = sum(p['ground truth'] == p['prediction'])/len(p)
tree.plot_tree(clf)

dot_data = tree.export_graphviz(clf, out_file=None)
graph = graphviz.Source(dot_data)
graph.render("wine")

dot_data = tree.export_graphviz(clf,
                                out_file=None,
                                feature_names=dataset.feature_names,
                                class_names=dataset.target_names,
                                filled=True,
                                rounded=True,
                                special_characters=True)
graph = graphviz.Source(dot_data)
graph.render("wine2")


# USING SVM
def use_svm(c):
    clf = svm.SVC(C=c)
    clf.fit(X_train, y_train)
    clf.predict(X_train)
    return clf.score(X_test, y_test)

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