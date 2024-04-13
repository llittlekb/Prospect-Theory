import pandas as pd
import numpy as np

My_max= pd.read_csv(r"data\output\Day_Return.csv",encoding='utf-8')
my_mon=pd.read_csv(r"data\input\Mon_Characteristics.csv",encoding='utf-8')

My_max = My_max.drop(['Ret'],axis=1)
My_max = My_max.drop(['VolumeRMB'],axis=1)
My_max["Day"] = pd.to_datetime(My_max["Day"])
My_max["Day"] = My_max["Day"].apply(lambda x: pd.Timestamp(year=x.year, month=x.month, day=28))
MAX_k3 = My_max.groupby(['Stock','Day']).agg({'Ret_t+1': lambda x: x.nlargest(3).mean()}).reset_index()
MAX_k3.rename(columns={'Ret_t+1':'MAX_k'},inplace=True)
MAX_k3.sort_values(by=["Stock","Day"],ascending=True,inplace=True)

##将月度数据的各类因子粘在一起
my_mon["Month"] = pd.to_datetime(my_mon["Month"],format="%Y%m%d") ##改变年月日格式
my_mon["Month"] = my_mon["Month"].apply(lambda x: x.replace(day=28))
MAX_k3.rename(columns={'Day':'Month','MAX_k':'MAX_k3'},inplace=True)
my_mon= pd.merge(my_mon,MAX_k3, on=['Stock','Month'], how='inner')
my_mon= my_mon.dropna(subset=['Return']).reset_index()
my_mon= my_mon.drop(['index'],axis=1)

#把收益率贴到t-1期
My=my_mon
Mon_MAX_k3 = My.dropna(subset=['MAX_k3']).reset_index()
Mon_MAX_k3['MAX_k3_lag']=Mon_MAX_k3['MAX_k3'].shift(1)
Mon_MAX_k3.loc[Mon_MAX_k3.groupby(['Stock'])['MAX_k3_lag'].head(1).index,'MAX_k3_lag'] = np.nan
Mon_MAX_k3 = Mon_MAX_k3.dropna(subset=['MAX_k3_lag']).reset_index()
Mon_MAX_k3=Mon_MAX_k3.drop(['index','level_0'],axis=1)

Mon_MAX_k3.to_csv(r"data\output\MAX_calculation\MAX_calculation.csv",index=False)



