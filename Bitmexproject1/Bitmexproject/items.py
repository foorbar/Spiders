# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BitmexprojectItem(scrapy.Item):
    id = scrapy.Field()
    timestamp = scrapy.Field()
    price = scrapy.Field()
    amount = scrapy.Field()
    buy_or_sell = scrapy.Field()
    # ------------以下为Kline数据-------------
    # symbol = scrapy.Field()
    # open = scrapy.Field()
    # high = scrapy.Field()
    # low = scrapy.Field()
    # close = scrapy.Field()
    # trades = scrapy.Field()
    # volume = scrapy.Field()
    # vwap = scrapy.Field()
    # lastSize = scrapy.Field()
    # turnover = scrapy.Field()
    # homeNotional = scrapy.Field()
    # foreignNotional = scrapy.Field()
    # timestamp = scrapy.Field()
    # binsize = scrapy.Field()

