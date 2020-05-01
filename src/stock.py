import pandas as pd
import requests
import mplfinance as mpf
import numpy as np
import datetime

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

        reformatted_data = dict()
        reformatted_data['Date'] = self.dates
        reformatted_data['Open'] = [float(i) for i in self.opens]
        reformatted_data['High'] = [float(i) for i in self.highs]
        reformatted_data['Low'] = [float(i) for i in self.lows]
        reformatted_data['Close'] = [float(i) for i in self.closes]
        reformatted_data['Volume'] = [float(i) for i in self.volumes]

        pdata = pd.DataFrame.from_dict(reformatted_data)
        pdata.set_index('Date', inplace=True)
        pdata.index = pd.to_datetime(pdata.index)

        data = data.transpose()
        data.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        data.index.name = 'Date'
        
        mpf.plot(pdata)
        
        
        #mpf.plot(data)
        

    def visualizeCandles(self):
        return

if __name__ == '__main__':
    stonk = Stock("CCL")
    stonk.updateStock("Daily")
    stonk.visualizeCandles()

    #print(stonk.opens[0])