# -*- coding: utf-8 -*-
"""
Created on Sat Jun  6 17:56:14 2020

@author: YeHui
"""

import os, rasterio
import numpy as np
from rasterio.windows import get_data_window

f_raster = r'D:\JJU\学生培养\A1651\fanweijiexian_Z\fanweijiexian\sjy250m_dem.tif'
# raster data with 5231 columns and 3201 rows
dat = []
idx = []
wid = []
with rasterio.open(f_raster) as src:
    print(src.block_size(1,0,0))
    # data = src.read() #all bands of the input dataset can be read into a 3-dimensonal ndarray
    for block_index, window in src.block_windows(1): # 1 was band of raster dataset
        block_array = src.read(window=window)
        dat.append(block_array)
        idx.append(block_index)
        wid.append(window)
        # r = src.read(1, window=window)
        # print(block_index)
    