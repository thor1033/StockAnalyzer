import pandas as pd
import requests

class Stock:
    
    def __init__(self, ticker):
        return
        #data = pd.read_json('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=' + ticker + '&apikey=BXAVNFY9YVG3DJDW')


    def updateStock(self, ticker):
        api_call = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol="+ ticker + "&apikey=BXAVNFY9YVG3DJDW"
        respond = requests.get(api_call)
        data = pd.DataFrame.from_dict(respond.json()['Time Series (Daily)'])
        print(data.head(10))

if __name__ == '__main__':
    stonk = Stock("IBM")
    stonk.updateStock('AAPL')