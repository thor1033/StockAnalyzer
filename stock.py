class Stock:
    
    def __init__(self, name, ticker, price, maxPrice, minPrice):
        self.name = name
        self.ticker = ticker
        self.currentPrice = price
        self.maxPrice = maxPrice
        self.minPrice = minPrice

    def updateStock(self, ticker):
        print(ticker)

if __name__ == '__main__':
    stonk = Stock("Apple", "APPL", 2300, 2400, 2200)
    stonk.updateStock('APPL')