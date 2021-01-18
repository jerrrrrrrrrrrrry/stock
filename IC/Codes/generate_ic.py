# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 21:47:43 2021

@author: admin
"""

import os
import sys
import datetime
import Config
sys.path.append(Config.GLOBALCONFIG_PATH)

import Global_Config as gc

import numpy as np
import pandas as pd
from pandas import Series, DataFrame

def main():
    #get y
    y1 = pd.read_csv('%s/Data/y1.csv'%gc.LABELBASE_PATH, index_col=[0], parse_dates=[0])
    
    #y2 = pd.read_csv('%s/Data/y2.csv'%gc.LABELBASE_PATH, index_col=[0], parse_dates=[0])
    #y3 = pd.read_csv('%s/Data/y3.csv'%gc.LABELBASE_PATH, index_col=[0], parse_dates=[0])
    #y4 = pd.read_csv('%s/Data/y4.csv'%gc.LABELBASE_PATH, index_col=[0], parse_dates=[0])
    #y5 = pd.read_csv('%s/Data/y5.csv'%gc.LABELBASE_PATH, index_col=[0], parse_dates=[0])
    
    #get factor
    files = os.listdir('%s/Data/'%gc.FACTORBASE_PATH)
    files = list(filter(lambda x:x[0] > '9', files))
    factors = {file[:-4]:pd.read_csv('%s/Data/%s'%(gc.FACTORBASE_PATH, file), index_col=[0], parse_dates=[0]) for file in files}
    
    y1 = y1.loc[factors[files[0][:-4]].index, factors[files[0][:-4]].columns]
    y1 = y1.subtract(y1.mean(1), axis=0).div(y1.std(1), axis=0)
    #ic
    ic = DataFrame({factor:(factors[factor] * y1).mean(1) for factor in factors.keys()})
    ic.to_csv('%s/Results/IC.csv'%gc.IC_PATH)
if __name__ == '__main__':
    main()