import pandas as pd
import numpy as np

Mon_MAX_k3 = pd.read_csv(r"data\output\MAX_calculation\MAX_calculation.csv",encoding='utf-8')

Mon_MAX_k3['MAX_k3_Rank'] = Mon_MAX_k3.groupby('Month')['MAX_k3_lag'].transform(lambda x:pd.qcut(x,5, labels=['SmallSize',2,3,4,'BigSize']))#根据滞后一期的Size，分月度进行分组
Mon_MAX_k3_ret = Mon_MAX_k3.groupby(['Month','MAX_k3_Rank']).agg({'Return':lambda x:x.mean()}).reset_index()#分月度计算组合平均收益率
Mon_MAX_k3_ret = Mon_MAX_k3_ret.pivot(index='Month', columns='MAX_k3_Rank', values='Return')#表格转置，以便计算多空组合收益
Mon_MAX_k3_ret['Small-big'] = Mon_MAX_k3_ret['SmallSize'] - Mon_MAX_k3_ret['BigSize']#计算多空组合收益率
MAX_k3_mean = Mon_MAX_k3_ret.mean()#计算组合收益率均值
MAX_k3_std  = Mon_MAX_k3_ret.std()#计算组合收益率标准差
t_stats = []#创建一个空的列表储存t统计量
n = Mon_MAX_k3_ret.count()#获取每一列的样本数量
for col in Mon_MAX_k3_ret.columns:#遍历每一列的索引
    t_stat = MAX_k3_mean[col]/(MAX_k3_std[col]/np.sqrt(n[col]))#计算t统计量
    t_stats.append(t_stat)#将各个组合的t统计量存入列表
MAX_k3_result = pd.DataFrame({'MAX_k3_mean':MAX_k3_mean,'MAX_k3_t':t_stats})#将均值和t统计量保存到一个dataframe中
MAX_k3_result['MAX_K3_mean'] = MAX_k3_result['MAX_k3_mean'].apply(lambda x: '{:.2%}'.format(x))#将均值转化为百分数，并保留两位小数
print(MAX_k3_result)
print("### Portfolio return is calculated")

