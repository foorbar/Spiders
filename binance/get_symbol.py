#!/usr/bin/env	python 
# _*_ coding:utf-8 _*_
import requests
import json


def getSymbol():
    url = 'https://api.binance.com/api/v1/exchangeInfo'
    response = requests.get(url)
    results = json.loads(response.content)
    symbols = results['symbols']
    for symbol in symbols:
        single_symbol = symbol['symbol']
        print(single_symbol)


if __name__ == '__main__':
    getSymbol()

