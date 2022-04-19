This small project deals with 3 types of ML algorithms: 
Naive Bayes, Decision Trees and Support Vector Machines. 
It compares their performance in sample cases, and explores how their
performance is affected changing their settings and hyperparameters in other cases.

The script ```compares_algos``` uses the scikit learn sample datasets and
applies the 3 algos to it, returning a dataframe with the scores. The dataset can be chosen from 
a limited set, documented in the settings.py module.
The datasets 'wine', 'iris', 'digits' and 'breast cancer' are to be used for a classification problem.
The 'diabetes' dataset is for use in a regression problem,
The 'linnerud' is a multi-output classification dataset, and at the moment is not handled in these scripts.

The script ```DT_explorator``` changes some parameters of a Decision Tree Classifier, to explore 
what happens, and plots some graphs. The dataset can be changes as a parameter at the top of the file.

The script ```SVM_explorator``` changes the penalty parameter C in a basic SVM model (SVC: Support Vector Classifier), 
and see what happens at the scores, plotting some graphs as per the DT_explorator. 
The 'iris' dataset can be changed as a parameter on the top.
Momentanously, the script is not ready to explore SVR regressors, hence the dataset must be chosen between the ones
for classification. 
Linear SVC and nu-SVC are included in the code for future use.
