#!/usr/bin/env	python 
# _*_ coding:utf-8 _*_
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
today_buy_amount = 0
for total_buy in today_buys:
    a_amount = total_buy['amount']
    today_buy_amount += float(a_amount)
today_sells = my_set.find({'time': {'$gte': today_timestamp, '$lte': today_timestamp+86400000}, 'buy_or_sell': 'sell'})
today_sell_amount = 0
for today_sell in today_sells:
    b_amount = today_sell['amount']
    today_sell_amount += float(b_amount)
yest_buys = my_set.find({'time': {'$gte': today_timestamp-86400000, '$lte': today_timestamp}, 'buy_or_sell': 'buy'})
yest_buy_amount = 0
for yest_buy in yest_buys:
    c_amount = yest_buy['amount']
    yest_buy_amount += float(c_amount)
yest_sells = my_set.find({'time': {'$gte': today_timestamp-86400000, '$lte': today_timestamp}, 'buy_or_sell': 'sell'})
yest_sell_amount = 0
for yest_sell in yest_sells:
    d_amount = yest_sell['amount']
    yest_sell_amount += float(d_amount)
last_week_buys = my_set.find({'time': {'$gte': today_timestamp-7*86400000, '$lte': today_timestamp-6*86400000}, 'buy_or_sell': 'buy'})
last_week_buy_amount = 0
for last_week_buy in last_week_buys:
    e_amount = last_week_buy['amount']
    last_week_buy_amount += float(e_amount)
last_week_sells = my_set.find({'time': {'$gte': today_timestamp-7*86400000, '$lte': today_timestamp-6*86400000}, 'buy_or_sell': 'sell'})
last_week_sell_amount = 0
for last_week_sell in last_week_sells:
    f_amount = last_week_sell['amount']
    last_week_sell_amount += float(f_amount)
today_total = float('%.2f' % (today_buy_amount + today_sell_amount))   # 今日总量
yest_total = float('%.2f' % (yest_buy_amount + yest_sell_amount))   # 昨天总量
last_week_total = float('%.2f' % (last_week_buy_amount + last_week_sell_amount))   # 上周该天总量
today_yest_total = '%.2f%%' % ((today_total-yest_total)/yest_total)   # 今天总量较昨天总量增长百分比
todal_last_week_total = '%.2f%%' % ((today_total-last_week_total)/last_week_total)    # 今天总量较上周该天总量增长百分比
today_yest_buy = '%.2f%%' % ((today_buy_amount-yest_buy_amount)/yest_buy_amount)     # 今天买入的总量较昨天买入总量的增长百分比
today_last_week_buy = '%.2f%%' % ((today_buy_amount-last_week_buy_amount)/last_week_buy_amount)      # 今天买入的总量较上周该天买入总量的百分比
today_yest_sell = '%.2f%%' % ((today_sell_amount-yest_sell_amount)/yest_sell_amount)   # 今天卖出的总量较昨天卖出总量的增长百分比
today_last_week_sell = '%.2f%%' % ((today_sell_amount-last_week_sell_amount)/last_week_sell_amount)  # 今天卖出的总量较上周该天卖出总量的增长百分比
# print(today_yest_total, todal_last_week_total, today_yest_buy, today_last_week_buy, today_yest_sell, today_last_week_sell)
today_buy_amount = float('%.2f' % (today_buy_amount))
today_sell_amount = float('%.2f' % (today_sell_amount))
timeArray = time.localtime((today_timestamp+86400000)/1000)
tomor_date = time.strftime("%Y-%m-%d %H:%M", timeArray)
# attr = ["买入", "卖出"]
# v1 = [today_buy_amount, today_sell_amount]
# pie = Pie("币安BTCUSDT", "{}~{} 交易额(币数)".format(today_date, tomor_date))
# pie.add("", attr, v1, is_label_show=True)
# pie.render()
print('BTC总交易币数{}个，较昨日增长{}，较上周增长{}；'
      '其中主动买进{}个，较昨日增长{}，较上周增长{}；'
      '主动卖出{}个，较昨日增长{}，较上周增长{}。'.format(today_total, today_yest_total, todal_last_week_total,
                                                today_buy_amount, today_yest_buy, today_last_week_buy,
                                                today_sell_amount, today_yest_sell, today_last_week_sell))
