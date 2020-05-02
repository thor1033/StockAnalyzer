import pandas as pd
import requests
import mplfinance as mpf
import numpy as np
import datetime

class Stock:
    
    def __init__(self, ticker):
        self.ticker = ticker


    def updateStock(self, CandleTypes = "Daily", size = "compact"): # CandleTypes [Daily, 1min, 5min, 15min, 30min, 60min]
        if(CandleTypes == "Daily"):
            api_call = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol="+ self.ticker + "&outputsize=" + size + "&apikey=BXAVNFY9YVG3DJDW"
        else:
            api_call = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=" + self.ticker + "&interval=" + CandleTypes + "&outputsize=" + size + "&apikey=BXAVNFY9YVG3DJDW"

        respond = requests.get(api_call)
        data = pd.DataFrame.from_dict(respond.json()['Time Series ('+CandleTypes+')'])
        self.opens = data.iloc[0].values
        self.highs = data.iloc[1].values
        self.lows = data.iloc[2].values
        self.closes = data.iloc[3].values
        self.volumes = data.iloc[4].values
        self.dates = data.axes[1]
        

    def visualizeCandles(self):
        #https://blog.csdn.net/wuwei_201/article/details/105783640
        #https://blog.csdn.net/wuwei_201/article/details/105815728?utm_medium=distribute.pc_relevant_right.none-task-blog-BlogCommendFromBaidu-1&depth_1-utm_source=distribute.pc_relevant_right.none-task-blog-BlogCommendFromBaidu-1
        reformatted_data = dict()
        reformatted_data['Date'] = list(reversed(self.dates))
        reformatted_data['Open'] = list(reversed([float(i) for i in self.opens]))
        reformatted_data['High'] = list(reversed([float(i) for i in self.highs]))
        reformatted_data['Low'] = list(reversed([float(i) for i in self.lows]))
        reformatted_data['Close'] = list(reversed([float(i) for i in self.closes]))
        reformatted_data['Volume'] = list(reversed([float(i) for i in self.volumes]))

        pdata = pd.DataFrame.from_dict(reformatted_data)
        pdata.set_index('Date', inplace=True)
        pdata.index = pd.to_datetime(pdata.index)
        
        my_color = mpf.make_marketcolors(up='cyan', down='red', edge='black', wick='black', volume='blue')
        my_style = mpf.make_mpf_style(marketcolors=my_color, gridaxis='both', gridstyle='-.', y_on_right=True)

        mpf.plot(pdata, type='candle', mav = (3,6,9), style=my_style, volume=True)

if __name__ == '__main__':
    #https://github.com/shirosaidev/stocksight for inspirations
    stonk = Stock("MED")
    stonk.updateStock("Daily", "full")
    stonk.visualizeCandles()