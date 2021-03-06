#!/usr/bin/env python
# coding: utf-8

#%%
import sys
import datetime
import numpy as np
import pandas as pd
from pandas import Series, DataFrame
import matplotlib.pyplot as plt
import tushare as ts
import os
import Config
sys.path.append(Config.GLOBALCONFIG_PATH)
from SingleFactor import SingleFactor
import Global_Config as gc
import tools
#%%

class skewHF(SingleFactor):
    def generate_factor(self):
        
        trade_cal = tools.get_trade_cal(self.start_date, self.end_date)
        skew = DataFrame()
        for date in trade_cal:
            r_daily = DataFrame()
            files = os.listdir('%s/StockSnapshootData/%s'%(gc.DATABASE_PATH, date))
            try:
                data_dic = {file.split('.')[1]:pd.read_csv('%s/StockSnapshootData/%s/%s'%(gc.DATABASE_PATH, date, file), index_col=[0], parse_dates=[0]) for file in files}
            except:
                print(date)
            keys = list(data_dic.keys())
            for key in keys:
                if len(data_dic[key]) == 0:
                    del data_dic[key]
            price = DataFrame({'%s.SZ'%stock:data_dic[stock].loc[:, 'price'] for stock in data_dic.keys()})
            price.fillna(method='ffill', inplace=True)
            price = price.loc[(price.index>'%s093000'%(date.replace('-', ''))) & (price.index<'%s150100'%(date.replace('-', ''))), :]
            r_daily = np.log(price).diff()
            r_daily.fillna(0, inplace=True)
            skew_daily = r_daily.resample(rule='15T').sum().skew()
            skew = pd.concat([skew, DataFrame({date:skew_daily}).T], axis=0)
            print(skew)
        a = skew
        self.factor = a



#%%
if __name__ == '__main__':
    #获取股票
    stocks = tools.get_stocks()

    a = skewHF('skewHF', stocks=stocks, start_date='20210101', end_date='20210128')
    
    a.generate_factor()
    
    a.factor_analysis()
    
    
