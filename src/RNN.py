import keras
import tensorflow as tf
import pandas as pd
import numpy as np
import random

class RNN:
    """
    Reccurent Neural Network:
    https://towardsdatascience.com/stock-prediction-using-recurrent-neural-networks-c03637437578
    """
    def __init__(self, stock):
        d = []
        for x in range(len(stock.volumes)):
            p = []
            p.append(float(stock.opens[x]))
            p.append(float(stock.closes[x]))
            p.append(float(stock.highs[x]))
            p.append(float(stock.lows[x]))
            p.append(float(stock.volumes[x]))
            d.append(p)
        self.stockData = pd.DataFrame(data=d,
                                      index = stock.dates,
                                      columns = ["Open", "Close", "High", "Low", "Volume"])
        #print(self.stockData)


    def train(self):
        random.seed(42)

        self.stockData['H-L'] = self.stockData['High'] - self.stockData['Low']
        self.stockData['C-O'] = self.stockData['Close'] - self.stockData['Open']
        self.stockData['3day MA'] = self.stockData['Close'].shift(1).rolling(window = 3).mean()
        self.stockData['10day MA'] = self.stockData['Close'].shift(1).rolling(window = 10).mean()
        self.stockData['30day MA'] = self.stockData['Close'].shift(1).rolling(window = 30).mean()
        self.stockData['Std_dev'] = self.stockData['Close'].rolling(5).std()


        print(self.stockData.iloc[:,-1])


        model = keras.Sequential([
            keras.layers.Dense(4, activation="relu"),
            keras.layers.Dense(20, activation="relu"),
            keras.layers.Dense(1, activation="softmax")
        ])
        #model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
        #model.fit(X,y, epochs=5)

    def normalize(self):
        df = (self.stockData - self.stockData.min()) / self.stockData.max()
        self.stockData = df
    