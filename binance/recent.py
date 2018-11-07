#!/usr/bin/env	python
# _*_ coding:utf-8 _*_
import multiprocessing
import requests
import json
import time
from pymongo import MongoClient
import threading
'''根据所给symbol来获取最近的数据'''


def recent(symbol):

    # 通过更改symbol来获取不同交易对的最近的数据以及创建数据表
    settings = {
        'ip': '192.168.1.97',
        'port': 27017,
        'db_name': 'binance',
        'set_name': symbol
    }
    content = {'symbol': symbol, 'limit': 1000}
    url = 'https://api.binance.com/api/v1/trades'
    response = requests.get(url, params=content)
    time.sleep(2)
    results = json.loads(response.content)
    for result in results:
        id = result['id']
        price = result['price']
        amount = result['qty']
        timestamp = result['time']
        isBuyerMaker = result['isBuyerMaker']
        buy_or_sell = 'buy' if isBuyerMaker else 'sell'
        print(symbol, id, timestamp, price, amount, buy_or_sell)
        conn = MongoClient(settings['ip'], settings['port'])
        db = conn[settings['db_name']]
        my_set = db[settings['set_name']]
        if not my_set.find_one({'id': id}):
            my_set.insert({'id': id, 'time': timestamp, 'price': price, 'amount': amount, 'buy_or_sell': buy_or_sell})
            # 根据id来创建唯一索引，数据重复时会报错但不影响程序运行
            my_set.create_index([('id', 1)], background=True, unique=True)
            print('{} 存储成功'.format(id))
        else:
            print('{}数据已存在'.format(id))


if __name__ == '__main__':
    symbols = ['BTCUSDT', 'ETHUSDT', 'ETCUSDT', 'XRPUSDT', 'EOSUSDT', 'BNBUSDT']
    pool = multiprocessing.Pool(6)
    # 多进程
    thread = threading.Thread(target=pool.map, args=(recent, [symbol for symbol in symbols]))
    thread.start()
    thread.join()
    print('ending---------------')


