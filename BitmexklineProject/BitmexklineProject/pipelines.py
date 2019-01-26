# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
from scrapy.conf import settings


class BitmexklineprojectPipeline(object):
    def process_item(self, item, spider):
        return item


class SaveToMongoDBPipeline(object):

    def open_spider(self, spider):
        conn = MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = conn[settings['MONGODB_DB']]
        self.db = db
        self.conn = conn

    def process_item(self, item, spider):
        my_set = self.db[settings['MONGODB_SYMBOL']]
        symbol = item['symbol']
        timestamp = item['timestamp']
        open_price = float(item['open'])
        high_price = float(item['high'])
        low_price = float(item['low'])
        close_price = float(item['close'])
        trades = float(item['trades'])
        volume = float(item['volume'])
        vwap = float(item['vwap']) if item['vwap'] else None
        lastSize = float(item['lastSize']) if item['lastSize'] else None
        turnover = float(item['turnover'])
        homeNotional = float(item['homeNotional'])
        foreignNotional = float(item['foreignNotional'])
        binsize = item['binsize']
        if not my_set.find_one({'close_time': timestamp}):
            res = {'close_time': timestamp, 'open_price': open_price, 'high_price': high_price, 'low_price': low_price, 'close_price': close_price, 'trades': trades,
                   'volume': volume, 'vwap': vwap, 'lastsize': lastSize, 'turnover': turnover,
                   'homeNotional': homeNotional, 'foreignNotional': foreignNotional}
            my_set.insert(res)
            my_set.create_index([('close_time', 1)], background=True, unique=True)
            print('{} 存储成功'.format(timestamp))
        else:
            print('{} save fail'.format(timestamp))
        return item

    def close_spider(self, spider):
        self.conn.close()


class SaveToCSV(object):

    def process_item(self, item, spider):
        symbol = item['symbol']
        timestamp = item['timestamp']
        open_price = item['open']
        high = item['high']
        low = item['low']
        close = item['close']
        trades = item['trades']
        volume = item['volume']
        vwap = item['vwap']
        lastSize = item['lastSize']
        turnover = item['turnover']
        homeNotional = item['homeNotional']
        foreignNotional = item['foreignNotional']
        binsize = item['binsize']
        result = [str(symbol), str(timestamp), str(open_price), str(close), str(high), str(low), str(trades),
                  str(volume), str(vwap), str(lastSize), str(turnover), str(homeNotional), str(foreignNotional), str(binsize)]
        file_name = settings['MONGODB_SYMBOL']
        with open('{}.csv'.format(file_name), 'a')as f:
            f.write(','.join(result) + '\n')
            print('{} save successfully'.format(timestamp))
