import pandas as pd
import numpy as np

My= pd.read_csv(r"data\input\Day_Price_Volume.csv",encoding='utf-8')

##算股票日度收益率
My["Day"] = pd.to_datetime(My["Day"],format="%Y%m%d") ##改变年月日格式
My['Price_lag'] = My['AdjustedClosePrice'].shift(1) 
My.loc[My.groupby(['Stock']).head(1).index,'Price_lag'] = np.nan #将每只股票的第一期的价格滞后值设为空值
My['Ret'] = My['AdjustedClosePrice']/My['Price_lag']-1
My = My.dropna(subset=['Ret']).reset_index() #删除DataFrame中'Ret'列中包含缺失值的行，并重新设置DataFrame的索引
My = My.drop(['index','Price_lag'],axis=1)

##把收益率贴到t-1期
My['Ret_t+1'] = My.groupby('Stock')['Ret'].shift(1)
My = My.dropna(subset=['Ret_t+1']).reset_index()

My.to_csv(r"data\output\Day_Return.csv",index=False)



