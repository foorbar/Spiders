#!/usr/bin/env	python 
# _*_ coding:utf-8 _*_
from pymongo import MongoClient
import datetime
import time
from pyecharts import Pie

conn = MongoClient('192.168.1.97', 27017)
db = conn['binance']
my_set = db['BTCUSDT']
today_date = '2018-11-6 00:00'
d = datetime.datetime.strptime(today_date, "%Y-%m-%d %H:%M")
t = d.timetuple()
timestamp = int(time.mktime(t))
today_timestamp = int(int(str(timestamp) + str("%06d" % d.microsecond)) / 1000)
today_buys = my_set.find({'time': {'$gte': today_timestamp, '$lte': today_timestamp+86400000}, 'buy_or_sell': 'buy'})
today_buy_price = 0
for today_buy in today_buys:
    a_price = today_buy['price']
    a_amount = today_buy['amount']
    a_buy_price = float(a_price) * float(a_amount)
    today_buy_price += a_buy_price
today_sells = my_set.find({'time': {'$gte': today_timestamp, '$lte': today_timestamp+86400000}, 'buy_or_sell': 'sell'})
today_sell_price = 0
for today_sell in today_sells:
    b_price = today_sell['price']
    b_amount = today_sell['amount']
    b_sell_price = float(b_price) * float(b_amount)
    today_sell_price += b_sell_price
yest_buys = my_set.find({'time': {'$gte': today_timestamp-86400000, '$lte': today_timestamp}, 'buy_or_sell': 'buy'})
yest_buy_price = 0
for yest_buy in yest_buys:
    c_price = yest_buy['price']
    c_amount = yest_buy['amount']
    c_buy_price = float(c_price) * float(c_amount)
    yest_buy_price += c_buy_price
yest_sells = my_set.find({'time': {'$gte': today_timestamp-86400000, '$lte': today_timestamp}, 'buy_or_sell': 'sell'})
yest_sell_price = 0
for yest_sell in yest_sells:
    d_price = yest_sell['price']
    d_amount = yest_sell['amount']
    d_sell_price = float(d_price) * float(d_amount)
    yest_sell_price += d_sell_price
last_week_buys = my_set.find({'time': {'$gte': today_timestamp-7*86400000, '$lte': today_timestamp-6*86400000}, 'buy_or_sell': 'buy'})
last_week_buy_price = 0
for last_week_buy in last_week_buys:
    e_price = last_week_buy['price']
    e_amount = last_week_buy['amount']
    e_buy_price = float(e_price) * float(e_amount)
    last_week_buy_price += e_buy_price
last_week_sells = my_set.find({'time': {'$gte': today_timestamp-7*86400000, '$lte': today_timestamp-6*86400000}, 'buy_or_sell': 'sell'})
last_week_sell_price = 0
for last_week_sell in last_week_sells:
    f_price = last_week_sell['price']
    f_amount = last_week_sell['amount']
    f_sell_price = float(f_price) * float(f_amount)
    last_week_sell_price += f_sell_price

today_total = float('%.2f' % (today_buy_price + today_sell_price))
yest_total = float('%.2f' % (yest_buy_price + yest_sell_price))
last_week_total = float('%.2f' % (last_week_buy_price + last_week_sell_price))
today_yest_total = '%.2f%%' % ((today_total-yest_total)/yest_total)
today_last_week_total = '%.2f%%' % ((today_total-last_week_total)/last_week_total)
today_yest_buy = '%.2f%%' % ((today_buy_price-yest_buy_price)/yest_buy_price)
today_last_week_buy = '%.2f%%' % ((today_buy_price-last_week_buy_price)/last_week_buy_price)
today_yest_sell = '%.2f%%' % ((today_sell_price-yest_sell_price)/yest_sell_price)
today_last_week_sell = '%.2f%%' % ((today_sell_price-last_week_sell_price)/last_week_sell_price)
today_buy_price = float('%.2f' % (today_buy_price))
today_sell_price = float('%.2f' % (today_sell_price))
timeArray = time.localtime((today_timestamp+86400000)/1000)
tomor_date = time.strftime("%Y-%m-%d %H:%M", timeArray)
# attr = ["流入", "流出"]
# v1 = [today_buy_price, today_sell_price]
# pie = Pie("币安BTCUSDT", "{}~{} 日流入流出资金(金额)".format(today_date, tomor_date))
# pie.add("", attr, v1, is_label_show=True)
# pie.render()
# print(today_yest_total, today_last_week_total, today_yest_buy, today_yest_sell, today_last_week_buy, today_last_week_sell)
print('BTC总交易金额{}，较昨日增长{}，较上周增长{}；'
      '其中主动买进{}，较昨日增长{}，较上周增长{}；'
      '主动卖出{}，较昨日增长{}，较上周增长{}。'.format(today_total, today_yest_total, today_last_week_total,
                                                today_buy_price, today_yest_buy, today_last_week_buy,
                                                today_sell_price, today_yest_sell, today_last_week_sell))
# print(yest_buy_price, yest_sell_price)
