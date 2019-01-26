# -*- coding: utf-8 -*-
import scrapy
import json
import time
from ..items import BinanceklineItem
from scrapy.conf import settings
from pymongo import MongoClient
# 获取binance的Kline数据
# 获取不同symbol数据时，需要更换settings文件中的数据库表名


class BinanceklineSpider(scrapy.Spider):
    name = 'binancekline'
    allowed_domains = ['binance.com']
    start_urls = ['https://api.binance.com']
    # https://api.binance.com/api/v1/klines?symbol=BTCUSDT&interval=1m&startTime=1541088000000&limit=1000

    def start_requests(self):
        # 连接数据库，获得数据的起始时间
        conn = MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = conn[settings['MONGODB_DB']]
        my_set = db[settings['MONGODB_SYMBOL']]
        recent_data = my_set.find().sort([('open_time', -1)]).limit(1)
        start_time = 0
        for recent_time in recent_data:
            start_time = recent_time['open_time']
        # 以当前时间为结束时间
        end_time = int(time.time())*1000
        print(start_time, end_time)
        for startTime in range(start_time, end_time, 60000000):
            # 根据settings中的集合名来获得网址中的参数
            symbol = settings['MONGODB_SYMBOL'].split('_')[0]
            interval = settings['MONGODB_SYMBOL'].split('_')[1]
            url = 'https://api.binance.com/api/v1/klines?symbol={}&interval={}&startTime={}&limit=1000'\
                .format(symbol, interval, startTime)
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                meta={},
                dont_filter=True
            )

    def parse(self, response):
        results = json.loads(response.text)
        if len(results) != 0:
            for result in results:
                open_time = result[0]
                open_price = float(result[1])
                high_price = float(result[2])
                low_price = float(result[3])
                close_price = float(result[4])
                volume = float(result[5])
                close_time = result[6]
                item = BinanceklineItem()
                item['open_time'] = open_time
                item['open_price'] = open_price
                item['high_price'] = high_price
                item['low_price'] = low_price
                item['close_price'] = close_price
                item['volume'] = volume
                item['close_time'] = close_time
                yield item
        else:
            print('没有更多数据了。。。')

# 1542263520000 1542337705000
