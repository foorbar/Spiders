#!/usr/bin/env	python 
# _*_ coding:utf-8 _*_
import requests
import json
import time
import multiprocessing
import threading

# tBTCUSD, tETHUSD, tEOSUSD, tLTCUSD, tXRPUSD, tNEOUSD
symbol = 'tBTCUSD'
# 15m, 30m, 1h
timeframe = '15m'


def get_data(starttime):
    content = {'limit': 1000, 'start': starttime, 'sort': 1}
    url = 'https://api.bitfinex.com/v2/candles/trade:{}:{}/hist'.format(timeframe, symbol)
    time.sleep(2)
    response = requests.get(url, params=content)
    results = json.loads(response.content)
    if len(results) > 1:
        for result in results:
            # timestamp = result[0]
            # open_price = result[1]
            # close_price = result[2]
            # high_price = result[3]
            # low_price = result[4]
            # volume = result[5]
            print(result)


if __name__ == '__main__':
    pool = multiprocessing.Pool(6)
    timeStamp = time.time()
    end_time = int(timeStamp * 1000)
    thread = threading.Thread(target=pool.map,
                              args=(get_data, [starttime for starttime in range(1514736000000, end_time, 900000000)]))
    thread.start()
    thread.join()
    print('ending---------------')

