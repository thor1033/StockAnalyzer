import keras
from keras.layers import Dense
from keras.layers import Dropout
import tensorflow as tf
import pandas as pd
import numpy as np
import random
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

class RNN:
    """
    Reccurent Neural Network:
    https://towardsdatascience.com/stock-prediction-using-recurrent-neural-networks-c03637437578
    """
    def __init__(self, stock):
        self.stockData = stock.data.iloc[::-1]


    def train(self):
        random.seed(42)

        self.stockData['H-L'] = self.stockData['High'] - self.stockData['Low']
        self.stockData['C-O'] = self.stockData['Close'] - self.stockData['Open']
        self.stockData['3day MA'] = self.stockData['Close'].shift(1).rolling(window = 3).mean()
        self.stockData['10day MA'] = self.stockData['Close'].shift(1).rolling(window = 10).mean()
        self.stockData['30day MA'] = self.stockData['Close'].shift(1).rolling(window = 30).mean()
        self.stockData['Std_dev'] = self.stockData['Close'].rolling(5).std()

        self.stockData['Price_Rise'] = np.where(self.stockData['Close'].shift(-1) > \
                                                self.stockData['Close'], 1, 0)
        #Price_Rise is 1 is our output value, storing 1 when the closing price of tomorrow is greater than the closing price today

        #Drops every rows storing NaN values
        self.stockData = self.stockData.dropna()
        
        #Splitting the data
        X = self.stockData.iloc[: , 5: -1] #Takes all columns from the 5th column to 2nd last
        y = self.stockData.iloc[:, -1]

        split = int(len(self.stockData)*0.8)
        X_train, X_test, y_train, y_test = X[:split], X[split:], y[:split], y[split:]

        #Feature scaling
        sc = StandardScaler()
        X_train = sc.fit_transform(X_train)
        X_test = sc.fit_transform(X_test) 
        #The y sets contains binary values and will therefore not be scalled

        classifier = keras.Sequential()
        classifier.add(Dense(units=128, kernel_initializer='uniform', activation='relu', input_dim = X.shape[1]))
        classifier.add(Dense(units=128, kernel_initializer='uniform', activation='relu'))
        classifier.add(Dense(units=1, kernel_initializer='uniform', activation='sigmoid'))
        classifier.compile(optimizer= 'adam', loss='mean_squared_error', metrics=['accuracy'])
        classifier.fit(X_train, y_train, batch_size=10, epochs=100)

        result = classifier.evaluate(X_test, y_test)
        
        y_pred = classifier.predict(X_test)
        y_pred = (y_pred > 0.5)

        self.stockData['y_pred'] = np.NaN
        self.stockData.iloc[(len(self.stockData)- len(y_pred)):, -1:] = y_pred
        trade_dataset = self.stockData.dropna()

        trade_dataset['Tomorrows Returns'] = 0.
        trade_dataset['Tomorrows Returns'] = np.log(trade_dataset['Close']/trade_dataset['Close'].shift(1))
        trade_dataset['Tomorrows Returns'] = trade_dataset['Tomorrows Returns'].shift(-1)

        trade_dataset['Strategy Returns'] = 0.
        trade_dataset['Strategy Returns'] = np.where(trade_dataset['y_pred'] == True, trade_dataset['Tomorrows Returns'], -trade_dataset['Tomorrows Returns'])
        
        trade_dataset['Cumulative Market Returns'] = np.cumsum(trade_dataset['Tomorrows Returns'])
        trade_dataset['Cumulative Strategy Returns'] = np.cumsum(trade_dataset['Strategy Returns'])

        plt.figure(figsize=(10,5))
        plt.plot(trade_dataset["Cumulative Market Returns"], color='r', label="Market Returns")
        plt.plot(trade_dataset["Cumulative Strategy Returns"], color='g', label="Strategy Returns")
        plt.legend()
        plt.show()

    def normalize(self):
        df = (self.stockData - self.stockData.min()) / self.stockData.max()
        self.stockData = df
    
