import pandas as pd
import numpy as np

my_mon=pd.read_csv(r"data\input\Mon_Characteristics.csv",encoding='utf-8')

##定义计算TK值所需要的函数
##价值函数
def v_func(x):
    if x>0:
        return x**0.88;
    else:
        return -2.25*((-x)**0.88)

##概率加权函数
def w_func_posi(p):
    w=(p**0.61)/(p**0.61+(1-p)**0.61)**(1/0.61)
    return w

def w_func_nega(p):
    w=(p**0.69)/(p**0.69+(1-p)**0.69)**(1/0.69)
    return w

My_TK = my_mon
r_free = My_TK.groupby(['Month']).agg({'Return': lambda x: x.mean()}).reset_index()
r_free.rename(columns={'Return':'r_free'},inplace=True)
My_TK= pd.merge(My_TK,r_free, on='Month', how='inner')
My_TK['unexpected_return']=My_TK['Return']-My_TK['r_free']

##计算TK值
#屏蔽警告
import warnings
warnings.filterwarnings("ignore")

stk_list = My_TK.drop_duplicates(subset='Stock',keep='first')
stk_list=list(stk_list['Stock'].values)##得到股票列表
#print(stk_list)
stk_list
mytk=pd.DataFrame()
for i in stk_list:
    all_mon=My_TK[My_TK['Stock']==i]
    mon_list = all_mon.drop_duplicates(subset='Month',keep='first')
    mon_list=list(mon_list['Month'].values)##得到月份列表
    t=0
    for k in range(len(mon_list)+1):
        if k>60:
            mon_60=pd.DataFrame()
            for j in range(60):
                mon_t= all_mon[all_mon['Month'] == mon_list[t+j]]
                mon_60= mon_60.append(mon_t)
            t=t+1
            mon_60.sort_values(by='unexpected_return',ascending=True,inplace=True)
            mon_60=mon_60.reset_index()
            mon_60 =mon_60.drop(['index'],axis=1)
            un_r_60=list(mon_60['unexpected_return'].values)
            c = [x for x in un_r_60 if x < 0]
            nega=len(c)#负收益月份数
            posi=60-nega#正收益月份数
            TK=0
            for z in range(len(un_r_60)):
                if z<nega:
                    tk=v_func(un_r_60[z])*(w_func_nega((z+1)/60)-w_func_nega((z+2)/60))
                    TK=TK+tk
                else:
                    tk=v_func(un_r_60[z])*(w_func_posi((posi+1-(1+z-nega))/60)-w_func_posi((posi-(1+z-nega))/60))
                    TK=TK+tk
            tk=pd.DataFrame([{'Stock':i,'Month':mon_list[k-1],'TK':TK}])
            mytk=mytk.append(tk)
    print(i)

mytk=mytk.reset_index()
mytk=mytk.drop(['index','level_0'],axis=1)
My_TK_mon= pd.merge(mytk,My_TK, on=['Stock','Month'], how='left')
My_TK_mon.to_csv(r"data\output\TK_calculation\tk_mon.csv",index=False)