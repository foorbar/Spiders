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
today_buy = my_set.find({'time': {'$gte': today_timestamp, '$lte': today_timestamp+86400000}, 'buy_or_sell': 'buy'}).count()
today_sell = my_set.find({'time': {'$gte': today_timestamp, '$lte': today_timestamp+86400000}, 'buy_or_sell': 'sell'}).count()
yest_buy = my_set.find({'time': {'$gte': today_timestamp-86400000, '$lte': today_timestamp}, 'buy_or_sell': 'buy'}).count()
yest_sell = my_set.find({'time': {'$gte': today_timestamp-86400000, '$lte': today_timestamp}, 'buy_or_sell': 'sell'}).count()
last_week_buy = my_set.find({'time': {'$gte': today_timestamp-7*86400000, '$lte': today_timestamp-6*86400000}, 'buy_or_sell': 'buy'}).count()
last_week_sell = my_set.find({'time': {'$gte': today_timestamp-7*86400000, '$lte': today_timestamp-6*86400000}, 'buy_or_sell': 'sell'}).count()
today_total = today_buy + today_sell
yest_total = yest_buy + yest_sell
last_week_total = last_week_buy + last_week_sell
today_yest_total = '%.2f%%' % ((today_total-yest_total)/yest_total)  # 今日较昨天总数增长百分比
todal_last_week_total = '%.2f%%' % ((today_total-last_week_total)/last_week_total)  # 今天较上周该天总数增长百分比
today_yest_buy = '%.2f%%' % ((today_buy-yest_buy)/yest_buy)   # 今日较昨天买进总数的增长百分比
today_last_week_buy = '%.2f%%' % ((today_buy-last_week_buy)/last_week_buy)   # 今日较上周该天买进总数的增长百分比
today_yest_sell = '%.2f%%' % ((today_sell-yest_sell)/yest_sell)   # 今日较昨天卖出总数的增长百分比
today_last_week_sell = '%.2f%%' % ((today_sell-last_week_sell)/last_week_sell)   # 今日较上周该天卖出总数的增长百分比
timeArray = time.localtime((today_timestamp+86400000)/1000)
tomor_date = time.strftime("%Y-%m-%d %H:%M", timeArray)
# attr = ["主动买", "主动卖"]
# v1 = [today_buy, today_sell]
# pie = Pie("币安BTCUSDT", "{}~{} 交易热度(笔数)".format(today_date, tomor_date))
# pie.add("", attr, v1, is_label_show=True)
# pie.render()
print('BTC总交易笔数{}笔，较昨日增长{}，较上周增长{}；'
      '其中主动买进{}笔，较昨日增长{}，较上周增长{}；'
      '主动卖出{}笔，较昨日增长{}，较上周增长{}'.format(today_total, today_yest_total, todal_last_week_total,
                                               today_buy, today_yest_buy, today_last_week_buy,
                                               today_sell, today_yest_sell, today_last_week_sell))
# 11.4 00:00 1541260800000
# 11.5 00:00 1541347200000
# 11.3 00:00 1541174400000
# 10.28 00:00 1540656000000
# 10.29 00:00 1540742400000

