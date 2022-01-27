from Machine_Learning_algos import load_sample_datasets as lsd
from sklearn import tree
import graphviz
import pandas as pd
from matplotlib import pyplot as plt

# LOADING DATASET
X_train, X_test, y_train, y_test, df = lsd.load_data(which='wine')

# TRAINING AND PREDICTING
clf = tree.DecisionTreeClassifier(criterion='gini',
                                  splitter='best',
                                  max_depth=3,
                                  min_samples_split=2,
                                  min_samples_leaf=1,
                                  min_weight_fraction_leaf=0.0,
                                  max_features=None,
                                  random_state=None,
                                  max_leaf_nodes=None,
                                  min_impurity_decrease=0.0,
                                  class_weight=None,
                                  ccp_alpha=0.0,
                                  )

# EXPLORING CHANGES IN max_depth:
param = list(range(1, 30))
scores = []
for n in param:
    clf = tree.DecisionTreeClassifier(max_depth=n)
    clf.fit(X_train, y_train, sample_weight=None)
    s = clf.score(X_test, y_test)
    scores.append(s)
    print(n, s)
plt.plot(param, scores, label='score vs. max depth')
plt.legend()

# EXPLORING CHANGES IN min_samples_split:
for n in range(2, 30):
    clf = tree.DecisionTreeClassifier(min_samples_split=n)
    clf.fit(X_train, y_train, sample_weight=None)
    s = clf.score(X_test, y_test)
    print(n, s)




clf = clf.fit(X_train, y_train, sample_weight=None)
prediction = clf.predict(X_test)

# VISUALISING RESULTS
score = clf.score(X_test, y_test)
p = pd.DataFrame(data=y_test, columns=['ground truth'])
p = p.assign(prediction=prediction)
p_score = sum(p['ground truth'] == p['prediction'])/len(p)
tree.plot_tree(clf)
dot_data = tree.export_graphviz(clf, out_file=None)
graph = graphviz.Source(dot_data)
graph.render("test_DT")
graph = graphviz.Sourcdot_data = tree.export_graphviz(
                                clf,
                                out_file=None,
                                feature_names=df.columns[:-1],
                                class_names=df.columns[-1],
                                filled=True,
                                rounded=True,
                                special_characters=True)
graph = graphviz.Source(dot_data)
graph.render("test_DT")

