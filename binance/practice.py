import xlrd
import matplotlib.pyplot as plt
buy = []
sell = []
a = 0  # 用于判断是否持仓，0代表空仓
xls = xlrd.open_workbook('hs300.xls')  # 打开文件
sheet = xls.sheets()[0]  # 打开表1
col = sheet.col_values(0)  # 打开第一列
ret = 0
nrows = sheet.nrows  # 行数
Sma = [0.0 for i in range(nrows)]
for j in range(19, nrows):   # 计算20日均线数值
    Sma[j] = sum(col[(j-19):(j+1)])/20
for k in range(19, nrows):   # 收盘价在20日均线之上，且均线是向上的，空仓的时候买入
    if Sma[k-1] < Sma[k] and col[k] > Sma[k] and a == 0:
        buy.append(col[k])
        a = 1
    elif col[k] < Sma[k] and Sma[k] < Sma[k-1] and a == 1:   # 收盘价在20日均线之下，且均线是向下的，持仓的时候卖出
        sell.append(col[k])
        a = 0
for l in range(0, len(sell)):  # 用卖出数列减去买入数列得到收益点数，然后对所有收益求和
    ret += sell[l]-buy[l]
print("总的收益点数：" "%.2f" % ret)  # 总的收益点数,绝对数值，不是百分比
plt.ylim(2000, 6000)
plt.plot(Sma[0:len(Sma)], 'r')
plt.plot(col, 'k')
