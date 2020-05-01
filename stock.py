import pandas as pd
import requests
import matplotlib.pyplot as plt
import plotly.graph_objects as go

class Stock:
    
    def __init__(self, ticker):
        self.ticker = ticker


    def updateStockDaily(self):
        api_call = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol="+ self.ticker + "&apikey=BXAVNFY9YVG3DJDW"
        respond = requests.get(api_call)
        data = pd.DataFrame.from_dict(respond.json()['Time Series (Daily)'])
        self.opens = data.iloc[0].values
        self.highs = data.iloc[1].values
        self.lows = data.iloc[2].values
        self.closes = data.iloc[3].values
        self.adjustedCloses = data.iloc[4].values
        self.volumes = data.iloc[5].values
        self.dividendAmount = data.iloc[6].values
        self.splitCoefficients = data.iloc[7].values
        self.dates = data.axes[1]

    def visualizeDailyCandles(self):
        fig = go.Figure(data=[go.Candlestick(x=self.dates,
                        open = self.opens,
                        high = self.highs,
                        low = self.lows,
                        close = self.closes)])
        fig.show()

if __name__ == '__main__':
    stonk = Stock("IBM")
    stonk.updateStockDaily()

    stonk.visualizeDailyCandles()

    print(stonk.opens)