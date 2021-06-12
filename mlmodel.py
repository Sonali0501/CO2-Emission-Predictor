import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import pickle

dataset = pd.read_csv('FuelConsumptionCo2.csv')
X = dataset.iloc[:, 4:6].values
X = np.concatenate((X,dataset.iloc[:, 10:11].values),axis=1) 
Y = dataset.iloc[:, -1].values


regressor = LinearRegression()

regressor.fit(X, Y)

pickle.dump(regressor, open('model.pkl','wb'))
