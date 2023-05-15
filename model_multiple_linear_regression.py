import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import hvplot.pandas
from sklearn import svm
from sklearn.model_selection import cross_val_score

from sklearn.model_selection import train_test_split

from sklearn.metrics import r2_score

from sklearn.linear_model import LinearRegression

import pickle as pkl

#%matplotlib inline
df=pd.read_csv('cleaned_data.csv')
df.head()
#df['province'] = df['province'].astype('category')
#df['province'] = df['province'].cat.codes
y = df['price']
x = df.drop(columns='price')

#======================================
#df = pd.read_csv("training_data.csv")
#sns.pairplot(data=df, diag_kind='kde')
#plt.show()
#======================================
#df = pd.read_csv("training_data.csv")
#sns.pairplot(df)
#plt.show()
#======================================

#print(df.corr()['price'])
x_train, x_test, y_train, y_test = train_test_split(x,y,test_size=0.40,random_state=0)
lr = LinearRegression()
lr.fit(x_train, y_train)
c = lr.intercept_
print("c: " + str(c))
m = lr.coef_
print("m: " + str(m))
y_pred_train = lr.predict(x_train)
#print("y_pred_train: " + str(y_pred_train))
#plt.scatter(y_train, y_pred_train)
#plt.xlabel("E - Precios Reales")
#plt.ylabel("E - Precios Previstos")
clf = svm.SVC(kernel='linear', C=0.01).fit(x_train, y_train)
clf.score(x_test, y_test)
clf = svm.SVC(kernel='linear', C=0.01, random_state=42)
scores = cross_val_score(clf, x, y, cv=5)
print("accuracy: "+ str(r2_score(y_train, y_pred_train)))
#plt.show()
###y_pred_test = lr.predict(x_test)
#plt.scatter(y_test, y_pred_test)
#plt.xlabel("T - Precios Reales")
#plt.ylabel("T - Precios Previstos")
#print(r2_score(y_test, y_pred_test))
#plt.show()
#89166.0,



#filenm = 'LR_model.pickle'
#Step 1: Create or open a file with write-binary mode and save the model to it
#pickle = pkl.dump(lr, open(filenm, 'wb'))#Step 2: Open the saved file with read-binary mode
#lr_pickle = pkl.load(open(filenm, 'rb'))#Step 3: Use the loaded model to make predictions 
#new_input = np.array([[1.0,1.5,78.0,5,1,1,1,0,0,1,1,0,1,0,0,0,0,1,0,0,1,0,0,1,1,0,0,0,1,0,0,1]])
#print(lr_pickle.predict(new_input))
####new_input = np.array([[1.0,1.5,78.0,5,1,1,1,0,0,1,1,0,1,0,0,0,0,1,0,0,1,0,0,1,1,0,0,0,1,0,0,1]])
####print(lr.predict(new_input))

#lr_pickle = pkl.load(open(filenm, 'rb'))#Step 3: Use the loaded model to make predictions 
#lr_pickle.predict([[300,85,5,5,5,8,1]])

