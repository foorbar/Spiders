# -*- coding: utf-8 -*-
import datetime
import random
import time
import json
import ssl
import requests
from functools import wraps
from pymongo import MongoClient
# 获取bitmex的k线数据
# 修改symbol时只需修改settings中的symbol即可


def sslwrap(func):
    @wraps(func)
    def bar(*args, **kw):
        kw['ssl_version'] = ssl.PROTOCOL_TLSv1
        return func(*args, **kw)
    return bar


ssl.wrap_socket = sslwrap(ssl.wrap_socket)

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

headers = {
    "x-firefox-spdy": "h2",
    "content-encoding": "gzip",
    "content-type": "application/json; charset=utf-8",
    "date": "Wed, 24 Oct 2018 02:46:55 GMT",
    "etag": "W/\"21248-H1rflx2v7eBIZjnIHTNjK66PepA\"",
    "strict-transport-security": "max-age=31536000; includeSubDomains",
    "x-powered-by": "Profit",
    "x-ratelimit-limit": "150",
    "x-ratelimit-remaining": "149",
    # "x-ratelimit-reset": "1540349216",
    'User-Agent': random.choice(USER_AGENTS),
}
# XBTUSD_1m, ETHUSD_1m, XBTZ18_1m, XBTH19_1m, XBTUSD_1d, XBTUSD_1h
settings = {
    'ip': '192.168.1.97',
    'port': 27017,
    'db_name': 'bitmex_kline',
    'set_name': 'XBTUSD_1h'
}
conn = MongoClient(settings['ip'], settings['port'])
db = conn[settings['db_name']]
my_set = db[settings['set_name']]


def parse_page(starttime):
    timeArray = time.localtime(starttime)
    date = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    symbol = settings['set_name'].split('_')[0]
    binsize = settings['set_name'].split('_')[1]
    real_url = 'https://www.bitmex.com/api/v1/trade/bucketed?binSize={}&partial=false&symbol={}&count=500&reverse=false&startTime={}'.format(
        binsize, symbol, date)
    with open('proxies.txt', 'r') as f:
        proxies = f.readlines()
        proxy = random.choice(proxies)[:-1]
        response = requests.get(real_url, headers=headers, proxies={'http': '{}'.format(proxy)})
        results = json.loads(response.text)
        if len(results) != 0:
            for result in results:
                # symbol = result['symbol']
                open_price = float(result['open']) if result['open'] else None
                high_price = float(result['high']) if result['high'] else None
                low_price = float(result['low']) if result['low'] else None
                close_price = float(result['close']) if result['close'] else None
                trades = float(result['trades'])
                volume = float(result['volume'])
                vwap = float(result['vwap']) if result['vwap'] else None
                lastSize = float(result['lastSize']) if result['lastSize'] else None
                turnover = float(result['turnover'])
                homeNotional = float(result['homeNotional'])
                foreignNotional = float(result['foreignNotional'])
                timeStamp = result['timestamp']
                timeStamp = timeStamp.replace('T', ' ').replace('Z', '').split('.')[0]
                d = datetime.datetime.strptime(timeStamp, "%Y-%m-%d %H:%M:%S")
                t = d.timetuple()
                timestamp = int(time.mktime(t))
                timestamp = int(int(str(timestamp) + str("%06d" % d.microsecond)) / 1000)
                # timestamp = '\'' + str(timestamp)
                if not my_set.find_one({'close_time': timestamp}):
                    res = {'close_time': timestamp, 'open_price': open_price, 'high_price': high_price,
                           'low_price': low_price, 'close_price': close_price, 'trades': trades,
                           'volume': volume, 'vwap': vwap, 'lastsize': lastSize, 'turnover': turnover,
                           'homeNotional': homeNotional, 'foreignNotional': foreignNotional}
                    my_set.insert(res)
                    my_set.create_index([('close_time', 1)], background=True, unique=True)
                    print('{} 存储成功'.format(timestamp))
                else:
                    print('{} save fail'.format(timestamp))
                # 存储到csv：
                # result = [str(timeStamp), str(open_price), str(high_price), str(low_price), str(close_price)]
                # with open('XBTUSD_1h1.csv', 'a')as file:
                #     file.write(','.join(result) + '\n')
                #     print('{} save successfully'.format(timeStamp))
            last_result = results[-1]
            the_time = last_result['timestamp']
            the_time = the_time.split('.')[0].replace('T', ' ')
            timeArray1 = time.strptime(the_time, "%Y-%m-%d %H:%M:%S")
            real_time = int(time.mktime(timeArray1)) + 1
            parse_page(real_time)
        else:
            print('没有更多数据了')


if __name__ == '__main__':
    start_datas = my_set.find().sort([('close_time', -1)]).limit(1)
    start_time = 0
    for start_data in start_datas:
        start_time = int(start_data['close_time']/1000)
    print(start_time)
    parse_page(start_time)
