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
            p.append(stock.opens[x])
            p.append(stock.closes[x])
            p.append(stock.highs[x])
            p.append(stock.lows[x])
            p.append(stock.volumes[x])
            d.append(p)
        self.stockData = pd.DataFrame(data=d,
                                      index = stock.dates,
                                      columns = ["Open", "Close", "High", "Low", "Volume"])
        #print(self.stockData)


    def train(self):
        print("dd")

    def normalize(self):
        #stacked_df = self.stockData.stack()
        #print(stacked_df)
        #dates = self.stockData.drop(columns = ["Dates"])
        print(self.stockData)
    