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

import Config
sys.path.append(Config.GLOBALCONFIG_PATH)
from SingleFactor import SingleFactor
import Global_Config as gc
import tools
#%%

class RQPM_HF(SingleFactor):
    def generate_factor(self):
        rqpm = pd.read_csv('%s/StockRQPMData/RQPMTHS.csv'%(gc.DATABASE_PATH), index_col=[0], parse_dates=[0])

        rqpm.columns = [col+'.SZ' for col in rqpm.columns]
        rqpm = rqpm.resample(rule='d').apply(lambda x:x.mean())
        a = rqpm
        a = a.loc[a.index >= self.start_date, :]
        a = a.loc[a.index <= self.end_date, :]
        self.factor = a



#%%
if __name__ == '__main__':
    #获取股票
    stocks = tools.get_stocks()

    a = RQPM_HF('RQPM_HF', stocks=stocks, start_date='20201201', end_date='20210128')
    
    a.generate_factor()
    
    a.factor_analysis()
    
    
