# -*- coding: utf-8 -*-
import scrapy
import json
import time
from ..items import BinanceklineItem
from scrapy.conf import settings
from pymongo import MongoClient
# 获取binance的Kline数据
# 获取不同symbol数据时，需要更换配置文件中的数据库表名

class BinanceklineSpider(scrapy.Spider):
    name = 'binancekline'
    allowed_domains = ['binance.com']
    start_urls = ['https://api.binance.com']
    # https://api.binance.com/api/v1/klines?symbol=BTCUSDT&interval=1m&startTime=1541088000000&limit=1000

    def start_requests(self):
        conn = MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = conn[settings['MONGODB_DB']]
        my_set = db[settings['MONGODB_SYMBOL']]
        recent_data = my_set.find().sort([('open_time', -1)]).limit(1)
        for recent_time in recent_data:
            start_time = recent_time['open_time']
            end_time = int(time.time())*1000
            print(start_time, end_time)
            for startTime in range(start_time, end_time, 60000000):
                symbol = settings['MONGODB_SYMBOL']
                url = 'https://api.binance.com/api/v1/klines?symbol={}&interval=1m&startTime={}&limit=1000'.format(symbol, startTime)
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
                open_price = result[1]
                high_price = result[2]
                low_price = result[3]
                close_price = result[4]
                volume = result[5]
                close_time = result[6]
                # print(open_time)
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

