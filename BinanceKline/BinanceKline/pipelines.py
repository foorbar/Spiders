# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.conf import settings
from pymongo import MongoClient


class BinanceklinePipeline(object):
    def process_item(self, item, spider):
        return item


class SaveToMongodbPipeline(object):

    def open_spider(self, spider):
        conn = MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = conn[settings['MONGODB_DB']]
        self.conn = conn
        self.db = db

    def process_item(self, item, spider):
        my_set = self.db[settings['MONGODB_SYMBOL']]
        open_time = item['open_time']
        open_price = item['open_price']
        high_price = item['high_price']
        low_price = item['low_price']
        close_price = item['close_price']
        volume = item['volume']
        close_time = item['close_time']
        if not my_set.find_one({'open_time': open_time}):
            res = {'open_time': open_time, 'open_price': open_price, 'high_price': high_price, 'low_price': low_price,
                   'close_price': close_price, 'volume': volume, 'close_time': close_time}
            my_set.insert(res)
            my_set.create_index([('open_time', 1)], background=True, unique=True)
            print('{} 存储成功'.format(open_time))
        else:
            print('{} save fail'.format(open_time))
        return item

    def close_spider(self, spider):
        self.conn.close()
