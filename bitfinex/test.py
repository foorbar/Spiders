#!/usr/bin/env	python
# -*- coding: utf-8 -*-
from pymongo import MongoClient
import ccxt
import time
# 获取bitfinex的k线数据


# BTC/USDT, ETH/USDT, EOS/USDT, LTC/USDT, XRP/USDT, NEO/USDT
symbol = 'XRP/USDT'
# 15m, 30m, 1h
timeframe = '30m'

set_name = symbol.replace('/', '') + '_' + timeframe
settings = {
    'ip': '192.168.1.97',
    'port': 27017,
    'db_name': 'bitfinex_kline',
    'set_name': set_name
}
conn = MongoClient(settings['ip'], settings['port'])
db = conn[settings['db_name']]
my_set = db[settings['set_name']]


def parse_page(starttime):
    bitfinex = ccxt.bitfinex()
    bitfinex.enableRateLimit = False
    results = bitfinex.fetch_ohlcv(symbol, timeframe, starttime, 1000)
    if len(results) > 1:
        for result in results:
            open_price = float(result[1]) if result[1] else None
            high_price = float(result[2]) if result[2] else None
            low_price = float(result[3]) if result[3] else None
            close_price = float(result[4]) if result[4] else None
            volume = float(result[5])
            timestamp = result[0]
            if not my_set.find_one({'timestamp': timestamp}):
                res = {'timestamp': timestamp, 'open_price': open_price, 'high_price': high_price,
                       'low_price': low_price, 'close_price': close_price, 'volume': volume}
                my_set.insert(res)
                my_set.create_index([('timestamp', 1)], background=True, unique=True)
                print('{} 存储成功'.format(timestamp))
            else:
                print('{} save fail'.format(timestamp))
            # print(timestamp, open_price, close_price, high_price, low_price)
            # 存储到csv：
            # result = [str(timeStamp), str(open_price), str(high_price), str(low_price), str(close_price)]
            # with open('XBTUSD_1h1.csv', 'a')as file:
            #     file.write(','.join(result) + '\n')
            #     print('{} save successfully'.format(timeStamp))
        last_result = results[-1]
        the_time = last_result[0]
        # print(the_time)
        time.sleep(2)
        parse_page(the_time)
    else:
        print('没有更多数据了')


if __name__ == '__main__':
    # start_datas = my_set.find().sort([('close_time', -1)]).limit(1)
    # start_time = 0
    # for start_data in start_datas:
    #     start_time = int(start_data['close_time']/1000)
    # print(start_time)
    # parse_page(1514736000000)
    parse_page(1539934200000)
