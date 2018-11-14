# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BitmexprojectItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()
    timestamp = scrapy.Field()
    price = scrapy.Field()
    amount = scrapy.Field()
    buy_or_sell = scrapy.Field()
