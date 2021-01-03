# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 14:44:48 2020

@author: YeHui
"""
import time, os
from multiprocessing import Pool
import multiprocessing
from osgeo import gdal
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.feature_selection import f_regression

fpath = r'E:/study/资料/数据/趋势与显著性水平'
rstDir = r'E:/study/资料/数据'

data_X = np.arange(1980, 2019, 1)
N = len(data_X) # time series for N years


def fun1(data_Y): # data_Y -> rasters for trend analysis
    df = pd.DataFrame({"cal": data_Y, "obs": data_X})
    df = df.dropna()
    if df.count()[0] < int(N * 2/3):  # number of data counts which is less than 1/3 of total set nan
        return np.nan, np.nan
    else:
        x_data = df['cal'].values
        y_data = df['obs'].values
        x_data = x_data.reshape(-1, 1)
        regr = LinearRegression()
        regr.fit(x_data, y_data)
        y_pred = regr.predict(x_data)
        r2score = r2_score(y_data, y_pred)
        pvalue = f_regression(x_data, y_data)[1][0]
        return pvalue, r2score


def gdal_write(file, data, ds):
    band1 = ds.GetRasterBand(1)
    img_datatype = band1.DataType
    driver = gdal.GetDriverByName('GTiff')
    out_ds = driver.Create(
        fpath + file,
        ds.RasterXSize,
        ds.RasterYSize,
        ds.RasterCount,
        img_datatype) # out_ds -> 
    out_ds.SetProjection(ds.GetProjection())
    out_ds.SetGeoTransform(ds.GetGeoTransform())
    for i in range(1, ds.RasterCount + 1):
        out_band = out_ds.GetRasterBand(i)
        out_band.WriteArray(data)
    out_ds.FlushCache()
    del out_ds


def fun(File1, File2, File3, File4, File5):
    if __name__ == '__main__':
        start = time.time()
        ds = gdal.Open(rstDir + os.sep + File1)
        im_width = ds.RasterXSize
        im_height = ds.RasterYSize
        # im_bands = ds.RasterCount
        # band1 = ds.GetRasterBand(1)
        # img_datatype = band1.DataType
        data1 = np.full((39, im_height * im_width), 1.0)
        for year in range(1980, 2019):
            file2 = rstDir + os.sep + File2 + str(year) + File3
            ds = gdal.Open(file2)
            img_data = ds.ReadAsArray()
            img_data = img_data.reshape(1, -1)
            data1[year - 1980] = img_data
        data1 = pd.DataFrame(data1).T
        data1 = data1.replace(np.inf, np.nan)
        data1 = data1.values
        cores = multiprocessing.cpu_count()
        pool = Pool(cores)
        data2 = pool.map(fun1, data1)
        data2 = pd.DataFrame(data2)
        data2 = data2.values
        data3 = data2[:, 0]
        data4 = data2[:, 1]
        data3 = data3.reshape(im_height, im_width)
        data4 = data4.reshape(im_height, im_width)
        gdal_write(File4, data3, ds)
        gdal_write(File5, data4, ds)
        end = time.time()
        print(end - start)


fun(r'IM/IM1980.tif', r'IM/IM', r'.tif', r'IM趋势.tif', r'IM显著性水平.tif')
