# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
from scrapy.conf import settings


class BitmexprojectPipeline(object):
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
        id = item['id']
        price = item['price']
        timestamp = item['timestamp']
        amount = item['amount']
        buy_or_sell = item['buy_or_sell']
        if not my_set.find_one({'id': id}):
            res = {'id': id, 'time': timestamp, 'price': price, 'amount': amount, 'buy_or_sell': buy_or_sell}
            my_set.insert(res)
            my_set.create_index([('id', 1)], background=True, unique=True)
            my_set.create_index([('time', 1)], background=True)
            print('{} 存储成功'.format(id))
        else:
            print('{} save fail'.format(id))
        return item

    def close_spider(self, spider):
        self.conn.close()
