import math
import statsmodels.api as sm
from linearmodels import FamaMacBeth 
import datetime
import pandas as pd
import numpy as np

My_TK_mon=pd.read_csv(r"data\output\TK_calculation\tk_mon.csv",encoding='utf-8')

df4=pd.DataFrame()
df4['Size']=My_TK_mon['Size']
My_TK_mon['excess_ret'] = My_TK_mon['Return'] - My_TK_mon['r_free']

fm1 = pd.DataFrame()
fm1['Stock'] = My_TK_mon['Stock']
fm1['Month'] = My_TK_mon['Month']
fm1['excess_ret'] = My_TK_mon['excess_ret']
fm1['TK'] = My_TK_mon['TK']
fm1['BM'] = My_TK_mon['BM']
fm1['Size'] = My_TK_mon['Size']

fm1['Month'] = pd.to_datetime(fm1['Month']) # 日期需设置为datetime格式
fm1 = fm1.set_index(['Stock', 'Month']) # 设置multi-index

mod = FamaMacBeth(fm1['excess_ret'], fm1[['TK','Size','BM']],check_rank=False)
## 一般fm回归结果展示的是Newey-West调整后的t值，.fit()中做如下设置
## 其中`bandwidth`是Newey-West滞后阶数，选取方式为lag = 4(T/100) ^ (2/9)
## 若不需要Newey-West调整则去掉括号内所有设置。
res = mod.fit()
print(res.summary)