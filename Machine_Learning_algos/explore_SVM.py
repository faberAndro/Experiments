import pandas as pd
from matplotlib import pyplot as plt
from sklearn import svm
from load_data import load_data

X_train, X_test, y_train, y_test, df = load_data()

# EXPLORING HINGE FUNCTION
from sklearn.datasets import make_blobs
X, y_true = make_blobs(n_samples=500, centers=2, cluster_std=0.7, random_state=0)
plt.scatter(X[:, 0], X[:, 1], s=20)

# PLOTTING SVM BEHAVIOURS TO DIFFERENT VALUES OF 'C':



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

sv = clf.support_vectors_
svi = clf.support_
svc = clf.n_support_
