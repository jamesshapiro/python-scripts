#!/usr/bin/env python3 -tt

import requests
import json

portfolio = json.loads('{"BTC": [REDACTED], "ETH": [REDACTED]}')
initial_investment = [REDACTED]

def extract_price(currency_symbol):
    url = "https://min-api.cryptocompare.com/data/price?fsym={}&tsyms=USD".format(currency_symbol)
    request = requests.get(url).text
    price_map = json.loads(request)
    price = float(price_map["USD"])
    return price

def compute_gains(portfolio):
    quantities = portfolio.values()
    prices = list(map(extract_price, portfolio.keys()))
    quantities_and_prices = zip(quantities, prices)
    
    portfolio_value = sum([quantity * price for (quantity, price) in quantities_and_prices])
    return portfolio_value - initial_investment

gains = compute_gains(portfolio)
print("gains = {}, {}%".format(round(gains, 2), round(100 * gains / initial_investment, 2)))

