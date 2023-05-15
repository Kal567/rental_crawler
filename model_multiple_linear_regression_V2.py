import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

data = pd.read_csv('cleaned_data.csv')

x = data.iloc[:, :-1].values
y = data.iloc[:, 1].values

regressor = LinearRegression()
regressor.fit(x, y)

y_pred = regressor.predict(x)

plt.scatter(x, y)
plt.plot(x, y_pred, color='red')
plt.show()