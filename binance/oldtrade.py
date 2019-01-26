#!/usr/bin/env	python
# -*- coding:utf-8 -*-
import json
import requests
import time
from pymongo import MongoClient
import threading
import multiprocessing
import random
# 解决OpenSSL.SSL.SysCallError: (-1, 'Unexpected EOF')错误
from DESAdapter import DESAdapter
# 解决EOF occurred in violation of protocol错误
import ssl
from functools import wraps
'''根据所给id来获取binance历史数据'''


def sslwrap(func):
    @wraps(func)
    def bar(*args, **kw):
        kw['ssl_version'] = ssl.PROTOCOL_TLSv1
        return func(*args, **kw)
    return bar


ssl.wrap_socket = sslwrap(ssl.wrap_socket)
#  不同的交易对的数据需要更换对应的symbol
# BNBUSDT, BTCUSDT, EOSUSDT, ETCUSDT, ETHUSDT, XRPUSDT
settings = {
    'ip': '192.168.1.97',
    'port': 27017,
    'db_name': 'binance',
    'set_name': 'BNBUSDT'
}
conn = MongoClient(settings['ip'], settings['port'])
db = conn[settings['db_name']]
USER_AGENTS = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10"
]


def get_oldtrade(fromId):
    # 请求该网址需要网站申请的api
    headers = {
        'X-MBX-APIKEY': 'TY9aVcqzvog44bnCItjBCpqXMZYwRtlPZ923rI8qXbgLfwB85NZmZGjMfdzxjMpO',
        'User-Agent': random.choice(USER_AGENTS),
    }
    content = {'symbol': settings['set_name'], 'fromId': fromId, 'limit': 1000}
    url = 'https://api.binance.com/api/v1/historicalTrades'
    with open('proxies.txt', 'r') as f:
        proxies = f.readlines()
        proxy = random.choice(proxies)[:-1]
        ses = requests.session()
        ses.mount('https://', DESAdapter())
        response = ses.get(url, params=content, headers=headers, proxies={'http': proxy})
        time.sleep(2)
        results = json.loads(response.content)
        if len(results) == 0:
            print('没有更多数据了')
        else:
            for result in results:
                trade_id = result['id']
                price = str(result['price'])
                amount = str(result['qty'])
                timestamp = result['time']
                isBuyerMaker = result['isBuyerMaker']
                buy_or_sell = 'buy' if isBuyerMaker else 'sell'
                res = {'id': trade_id, 'time': timestamp, 'price': price, 'amount': amount, 'buy_or_sell': buy_or_sell}
                print(trade_id, timestamp, price, amount, buy_or_sell)
                if not db[settings['set_name']].find_one({'id': trade_id}):
                    db[settings['set_name']].insert(res)
                    db[settings['set_name']].create_index([('id', 1)], background=True, unique=True)
                    print('{} 存储成功'.format(trade_id))
                else:
                    print('{} save fail'.format(trade_id))


if __name__ == '__main__':
    pool = multiprocessing.Pool(6)
    # 通过更改for循环来更改数据范围
    end_id = 0
    start_id = 0
    recent_datas = db[settings['set_name']].find().sort([('id', -1)]).limit(1)
    for recent_data in recent_datas:
        end_id = recent_data['id']
    start_datas = db[settings['set_name']].find().sort([('id', -1)]).skip(1000).limit(1)
    for start_data in start_datas:
        start_id = start_data['id']
    print(start_id, end_id)
    thread = threading.Thread(target=pool.map, args=(get_oldtrade,
                                                     [fromId for fromId in range(start_id, end_id, 1000)]))
    # 18353157 18364907
    thread.start()
    thread.join()
    print('ending---------------')



