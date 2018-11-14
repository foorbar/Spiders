# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BinanceklineItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    open_time = scrapy.Field()
    open_price = scrapy.Field()
    high_price = scrapy.Field()
    low_price = scrapy.Field()
    close_price = scrapy.Field()
    volume = scrapy.Field()
    close_time = scrapy.Field()
