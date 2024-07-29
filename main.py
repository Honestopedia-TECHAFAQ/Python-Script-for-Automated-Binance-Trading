from binance.client import Client
from binance.exceptions import BinanceAPIException
import time

API_KEY = 'your_api_key'
API_SECRET = 'your_api_secret'

client = Client(API_KEY, API_SECRET)

symbol = 'BTCUSDT'  
usdt_amount = 10  
profit_target = 0.03  
stop_loss = 0.01 
def get_price(symbol):
    """ Get the current price of the symbol """
    ticker = client.get_symbol_ticker(symbol=symbol)
    return float(ticker['price'])

def place_order(symbol, quantity):
    """ Place a market order """
    try:
        order = client.order_market_buy(
            symbol=symbol,
            quantity=quantity
        )
        return order
    except BinanceAPIException as e:
        print(f"Error placing order: {e}")
        return None

def place_oco_order(symbol, quantity, buy_price):
    """ Place an OCO order """
    try:
        price = buy_price
        stop_price = price * (1 - stop_loss)
        limit_price = price * (1 + profit_target)
        
        order = client.order_oco_sell(
            symbol=symbol,
            quantity=quantity,
            price=round(limit_price, 2),
            stopPrice=round(stop_price, 2),
            stopLimitPrice=round(stop_price * 1.01, 2),
            stopLimitTimeInForce='GTC'
        )
        return order
    except BinanceAPIException as e:
        print(f"Error placing OCO order: {e}")
        return None

def trade():
    """ Main trading logic """
    while True:
        price = get_price(symbol)
        quantity = usdt_amount / price
        buy_order = place_order(symbol, quantity)
        
        if buy_order:
            print(f"Buy order executed: {buy_order}")
            oco_order = place_oco_order(symbol, quantity, price)
            
            if oco_order:
                print(f"OCO order placed: {oco_order}")
            time.sleep(10)  

if __name__ == "__main__":
    trade()
