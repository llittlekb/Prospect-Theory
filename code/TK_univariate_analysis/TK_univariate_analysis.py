import pandas as pd
import numpy as np

My_TK_mon=pd.read_csv(r"data\output\TK_calculation\tk_mon.csv",encoding='utf-8')

My_TK_mon['tk_Rank'] = My_TK_mon.groupby('Month')['TK'].transform(lambda x:pd.qcut(x,5, labels=['SmallSize',2,3,4,'BigSize']))#根据滞后一期的Size，分月度进行分组
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