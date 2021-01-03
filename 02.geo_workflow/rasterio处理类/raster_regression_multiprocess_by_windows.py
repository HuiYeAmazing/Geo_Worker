# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 17:57:55 2020

@author: YeHui
"""
import os, rasterio, datetime
from glob import glob as glb
import numpy as np
from rasterio.windows import get_data_window
from multiprocessing import Pool
import multiprocessing
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.feature_selection import f_regression
import concurrent.futures

Ts = datetime.datetime.now()
dir_rasters = r'D:\f_work\C_workspace\Sanjy'
dest_folder = dir_rasters
year_set = 2001, 2017
var_str = 'NPP'
cond = [0, 2000]  # 数据有效范围
raster_type = 'flt'
f_coef = dest_folder + os.sep + var_str + '_coef.' + raster_type
f_r2score = dest_folder + os.sep + var_str + '_r2score.' + raster_type
f_pvalue = dest_folder + os.sep + var_str + '_pvalue.' + raster_type

var1_output = f_coef
var2_output = f_r2score
var3_output = f_pvalue
x_var_time = np.arange(year_set[0], year_set[1] + 1)  # 时间轴

N = len(x_var_time)  # time series for N years

def fun_myfun(data_1): # regression
    """
    :param data_1: 需要计算趋势和显著性水平的数组
    :return: 返回趋势r2score和显著性水平pvalue
    """
    x_data = data_1
    y_data = x_var_time
    x_data = x_data.reshape(-1, 1)
    regr = LinearRegression()
    regr.fit(x_data, y_data)
    y_pred = regr.predict(x_data)
    r2score = r2_score(y_data, y_pred)              # 趋势
    pvalue = f_regression(x_data, y_data)[1][0]     # 显著性水平
    return pvalue, r2score                          # 返回趋势和显著性水平

def Read_raster_by_window(arg_window):
    block_array_set = []
    for i, year in enumerate(list(x_var_time)):
        f_raster = glb(dir_rasters + os.sep + "*" + str(year) + "*." + raster_type)[0]
        with rasterio.open(f_raster) as src:
            if i == 0:
                profile = src.profile
                windows = [window for ij, window in src.block_windows()]
            block_array = src.read(window=arg_window)
        block_array_set.append(block_array)
        data = np.array(block_array_set)
        result = fun_myfun(data)
        with rasterio.open(var1_output, 'w', **profile) as dst1:
            dst1.write(result[0], window=arg_window)
        with rasterio.open(var2_output, 'w', **profile) as dst2:
            dst2.write(result[1], window=arg_windoww)
        with rasterio.open(var3_output, 'w', **profile) as dst3:
            dst3.write(result[2], window=arg_windoww)


with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    executor.map(Read_raster_by_window, windows)                          # 并发处理
# end = time.time()
# print(end - start)

