import pandas as pd
import requests
import mplfinance as mpf
import numpy as np
import datetime
import logging

class Stock:
    
    def __init__(self, ticker):
        self.ticker = ticker


    def updateStock(self, CandleTypes = "Daily", size = "compact"): # CandleTypes [Daily, 1min, 5min, 15min, 30min, 60min]
        if(CandleTypes == "Daily"):
            api_call = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol="+ self.ticker + "&outputsize=" + size + "&apikey=BXAVNFY9YVG3DJDW"
        else:
            api_call = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=" + self.ticker + "&interval=" + CandleTypes + "&outputsize=" + size + "&apikey=BXAVNFY9YVG3DJDW"

        try:
            respond = requests.get(api_call)
            data = pd.DataFrame.from_dict(respond.json()['Time Series ('+CandleTypes+')'])
            self.opens = data.iloc[0].values
            self.highs = data.iloc[1].values
            self.lows = data.iloc[2].values
            self.closes = data.iloc[3].values
            self.volumes = data.iloc[4].values
            self.dates = data.axes[1]
        except(requests.HTTPError, requests.ConnectionError, requests.ConnectTimeout) as re:
            logging.error("Exception: exception getting stockdata from url caused by %s" % re)
            raise
        
    def getTechInd(self, indType, interval, timePeriod = 10, seriesType = "open"):
        """
        indType = [SMA, EMA, WMA, DEMA, TEMA, TRIMA, KAMA, MAMA, VWAP, T3, MACD, MACDEXT, STOCH, STOCHF, RSI, STOCHRSI,
                   WILLR, ADX, ADXR, APO, PPO, MOM, BOP, CCI, CMO, ROC, ROCR, AROON, AROONSC, MFI, TRIX, ULTSC, DX,
                   MINUS_DI, PLUS_DI, MINUS_DM, PLUS_DM, BBANDS, MIDPOINT, MIDPRICE, SAR, TRANGE, ATR, NATR, AD, ADOSC,
                   OBV, HT_TRENDLINE, HT_SINE, HT_DCPERIOD, HT_DCPHASE, HT_PHASOR]
        interval = [1min, 5min, 15,min, 30min, 60min, daily, weekly, monthly]
        timePeriod = number of datapoints used to calculate each moving average value
        seriesType = [close, open, high, low]
        """
        api_call = "https://www.alphavantage.co/query?function=" + indType + "&symbol=" + self.ticker + "&interval=" + interval + "&time_period=" + str(timePeriod) + "&series_type= " + seriesType + "&apikey=BXAVNFY9YVG3DJDW"
        try:
            r = requests.get(api_call)
            data = pd.DataFrame.from_dict(r.json()['Technical Analysis: ' + indType])
            self.techInd = data.iloc[0].values
            self.techIndDates = data.axes[1]

        except(requests.HTTPError, requests.ConnectionError, requests.ConnectTimeout) as re:
            logging.error("Exception: exception getting stockdata from url caused by %s" % re)
            raise



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
    #stonk.updateStock("Daily", "full")
    stonk.getTechInd("EMA", "daily")
    #stonk.visualizeCandles()