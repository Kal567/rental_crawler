import pandas as pd
from sklearn.datasets import wine
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_score
from sklearn.metrics import classification_report
from sklearn.metrics import recall_score
from sklearn import tree
from matplotlib import pyplot as plt

data = load_breast_cancer()
dataset = pd.DataFrame(data=data['data'], columns=data['feature_names'])
#dataset.head()
x = dataset.copy()
y = data['target']
#y=y[dataset.isfinite(x[27])]
#x=x[dataset.isfinite(x[27])]
x_train, x_test, y_train, y_test = train_test_split(x,y,test_size=0.3)
clf = DecisionTreeClassifier(max_depth=4)
clf = clf.fit(x_test, y_train)
print(clf.get_params())
predictions = clf.predict(x_test)
clf.predict_proba(x_test)

accuracy_score(y_test, predictions, labels=[0,1])
#precision_score(y_test, predictions)
#print(classification_report(y_test, predictions, target_names=['malignant', 'benign']))
#x.shape[0]
#feature_names = x.columns
#print(feature_names)
#feature_importance = pd.DataFrame(clf.feature_importances_, index=feature_names)
#print(feature_importance)
#features = list(feature_importance[feature_importance[0].index])#.sort_values(1)
#print(features)
#feature_importance.head(10).plot(kind='bar')
#fig = plt.figure(figsize=(25,20))
#_ = tree.plot_tree(clf, feature_names=feature_names, class_names={0:'Malignant',
#                                                                  1: 'Benign'}, filled=True, fontsize=12)
#x_test.head()
#sparse = clf.decision_path(x_test).toarray()[:101]