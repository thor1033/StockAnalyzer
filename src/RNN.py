import keras
import tensorflow as tf
import pandas as pd

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
        print("dd")

    def normalize(self):
        df = (self.stockData - self.stockData.min()) / self.stockData.max()
        return df
    