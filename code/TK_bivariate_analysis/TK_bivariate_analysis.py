import pandas as pd
import numpy as np

My_TK_mon=pd.read_csv(r"data\output\TK_calculation\tk_mon.csv",encoding='utf-8')

all_day_list = My_TK_mon.drop_duplicates(subset='Month',keep='first')##去除时间上的重复值
all_day_list=list(all_day_list['Month'].values)##values获取列数据变成列表
data_t = pd.DataFrame()
number = 1

for i in all_day_list:
    data1 = My_TK_mon[My_TK_mon['Month']==i]
    data1['date'] = number
    data_t=data_t.append(data1)
    number = number+1

r3_total = pd.DataFrame()

for i in range(1,181):
    data1 = data_t[data_t['date']==i]
    data1['p1']=pd.qcut(data1['Size'],q=2,labels=False,duplicates='drop') 
    #使用pd.qcut()函数对data1中的'size'变量进行分位数离散化，将'size'变量分为3个区间，并使用数字0到4对这些区间进行编码，编码结果保存在新列'p1'中。
    r3_total=r3_total.append(data1)

My_TK_mon = r3_total[r3_total['p1']==0]
My_TK_mon['tk_Rank'] = My_TK_mon.groupby('Month')['TK'].transform(lambda x:pd.qcut(x,5, labels=['SmallSize',2,3,4,'BigSize']))
My_TK_mon_ret = My_TK_mon.groupby(['Month','tk_Rank']).agg({'Return':lambda x:x.mean()}).reset_index()#分月度计算组合平均收益率
My_TK_mon_ret = My_TK_mon_ret.pivot(index='Month', columns='tk_Rank', values='Return')#表格转置，以便计算多空组合收益
My_TK_mon_ret['Small-big'] = My_TK_mon_ret['SmallSize'] - My_TK_mon_ret['BigSize']#计算多空组合收益率
My_TK_mon_mean = My_TK_mon_ret.mean()#计算组合收益率均值
My_TK_mon_std  = My_TK_mon_ret.std()#计算组合收益率标准差
t_stats = []#创建一个空的列表储存t统计量
n = My_TK_mon_ret.count()#获取每一列的样本数量
for col in My_TK_mon_ret.columns:#遍历每一列的索引
    t_stat = My_TK_mon_mean[col]/(My_TK_mon_std[col]/np.sqrt(n[col]))#计算t统计量
    t_stats.append(t_stat)#将各个组合的t统计量存入列表
My_TK_mon_result = pd.DataFrame({'My_TK_mon_mean':My_TK_mon_mean,'My_TK_mon_t':t_stats})#将均值和t统计量保存到一个dataframe中
My_TK_mon_result['My_TK_mon_mean'] = My_TK_mon_result['My_TK_mon_mean'].apply(lambda x: '{:.2%}'.format(x))#将均值转化为百分数，并保留两位小数
print(My_TK_mon_result)
print("### Portfolio return is calculated")