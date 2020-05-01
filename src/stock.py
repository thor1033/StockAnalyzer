import pandas as pd
import requests
import matplotlib.pyplot as plt
import plotly.graph_objects as go

class Stock:
    
    def __init__(self, ticker):
        self.ticker = ticker


    def updateStock(self, CandleTypes = "Daily"): # CandleTypes [Daily, 1min, 5min, 15min, 30min, 60min]
        if(CandleTypes == "Daily"):
            api_call = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol="+ self.ticker + "&apikey=BXAVNFY9YVG3DJDW"
        else:
            api_call = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=" + self.ticker + "&interval=" + CandleTypes + "&apikey=BXAVNFY9YVG3DJDW"

        respond = requests.get(api_call)
        data = pd.DataFrame.from_dict(respond.json()['Time Series ('+CandleTypes+')'])
        self.opens = data.iloc[0].values
        self.highs = data.iloc[1].values
        self.lows = data.iloc[2].values
        self.closes = data.iloc[3].values
        self.volumes = data.iloc[4].values
        self.dates = data.axes[1]

    def visualizeCandles(self):
        fig = go.Figure(data=[go.Candlestick(x=self.dates,
                        open = self.opens,
                        high = self.highs,
                        low = self.lows,
                        close = self.closes)])
        fig.show()

if __name__ == '__main__':
    stonk = Stock("IBM")
    stonk.updateStock("Daily")
    stonk.visualizeCandles()

    print(stonk.opens[0])