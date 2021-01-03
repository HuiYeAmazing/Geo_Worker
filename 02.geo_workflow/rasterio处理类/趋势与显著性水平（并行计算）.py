import time
# 并行计算的库
from multiprocessing.dummy import Pool
import multiprocessing
# gdal库
from osgeo import gdal
# 关于数据处理的库
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.feature_selection import f_regression


def fun1(data_1):               # 计算趋势和显著性水平的函数
    # data_1为需要进行计算的数组
    data_2 = np.linspace(1980, 2019, 39)  # 建立关于年份的数组
    x_data = data_1
    y_data = data_2
    x_data = x_data.reshape(-1, 1)   # reshape(-1, 1)的意思是将数组转化为每行1列，自定义行数的数组
    regr = LinearRegression()
    regr.fit(x_data, y_data)
    y_pred = regr.predict(x_data)
    r2score = r2_score(y_data, y_pred)      # 趋势
    pvalue = f_regression(x_data, y_data)[1][0]     # 显著性水平
    return pvalue, r2score


def Write(file, data, ds):        # 将数组写入tif文件
    # file为tif文件名
    # data为写入的数组
    # ds为之前读取的tif文件，这里是为了和原来的tif文件的象元保持一致；
    band1 = ds.GetRasterBand(1)
    img_datatype = band1.DataType
    driver = gdal.GetDriverByName('GTiff')          # 明确写入数据驱动类型
    out_ds = driver.Create(
        r'E:/study/资料/数据/趋势与显著性水平/' + file,  # tif文件所保存的路径
        ds.RasterXSize,             # 行
        ds.RasterYSize,             # 列
        ds.RasterCount,             # 波段数
        img_datatype)               # 数据类型
    out_ds.SetProjection(ds.GetProjection())        # 投影信息
    out_ds.SetGeoTransform(ds.GetGeoTransform())    # 仿射信息
    for i in range(1, ds.RasterCount + 1):          # 循环逐波段写入
        out_band = out_ds.GetRasterBand(i)
        out_band.WriteArray(data)                   # 写入数据
    out_ds.FlushCache()
    del out_ds


def fun(File1, File2, File3, File4, File5):
    # 以路径E:/study/资料/数据/prcp_year/PRCP1980SUM.tif为例
    # File1为需要读取的tif文件的文件夹及文件名即r'prcp_year/PRCP1980SUM.tif'
    # File2为r'prcp_year/PRCP'
    # File3为r'SUM.tif'
    # File4为需要写入的趋势tif文件名，比如r'prcp趋势.tif'
    # File5为需要写入的显著性水平tif文件名，比如r'prcp显著性水平.tif'
    if __name__ == '__main__':          # 程序入口
        start = time.time()
        file1 = r'E:/study/资料/数据/'          # 需要读取的tif文件所在的文件夹的所在文件夹的路径
        ds = gdal.Open(file1 + File1)       # 打开文件
        # 影像数据基本情况 波段数、行、列等
        im_width = ds.RasterXSize       # 行
        im_height = ds.RasterYSize      # 列
        im_bands = ds.RasterCount       # 波段数
        # 影像数据读取
        band1 = ds.GetRasterBand(1)     # 波段的indice起始为1，不为0
        img_datatype = band1.DataType   # 数据类型
        data1 = np.full((39, im_height * im_width), 1.0)  # 建立数组
        for year in range(1980, 2019):
            file2 = file1 + File2 + str(year) + File3
            ds = gdal.Open(file2)
            img_data = ds.ReadAsArray()     # 读取整幅图像转化为数组
            img_data = img_data.reshape(1, -1)      # 将数组转化为1行，自定义列的数组
            data1[year - 1980] = img_data           # 将读取的数组合并成一个大数组
        # 将数组转换成以象元数为行数，年份为列数的数组
        data1 = pd.DataFrame(data1)
        data1 = data1.T
        data1 = data1.values
        # 多核并行计算
        cores = multiprocessing.cpu_count()     # 计算机cpu的核心数（核心数=线程数，但具有多线程技术和超线程技术的线程数一般为核心数的两倍）
        pool = Pool(cores)                      # 开启线程池
        data2 = pool.map(fun1, data1)           # 进行并行计算，得到的data2是一个列表，map是按行读取数组来计算
        # 将data2转换成对应数组
        data2 = pd.DataFrame(data2)
        data2 = data2.values
        data3 = data2[:, 0]
        data4 = data2[:, 1]
        data3 = data3.reshape(im_height, im_width)
        data4 = data4.reshape(im_height, im_width)
        # 写入文件
        Write(File4, data3, ds)
        Write(File5, data4, ds)
        end = time.time()
        print(end - start)


fun(r'prcp_year/PRCP1980SUM.tif', r'prcp_year/PRCP', r'SUM.tif', r'prcp趋势.tif', r'prcp显著性水平.tif')