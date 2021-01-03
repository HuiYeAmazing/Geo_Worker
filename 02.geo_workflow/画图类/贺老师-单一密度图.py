# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 20:43:24 2020

@author: eomf
"""
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
from scipy.stats import gaussian_kde
from sklearn.preprocessing import PolynomialFeatures
import statsmodels.api as sm
import math

#j = range(65,362,8)
j = 65
Yr='2018'
doy='%03d' %j
#将txt读成向量
df1=np.genfromtxt(r'C:\Users\eomf\Desktop\isctxt/'+Yr+doy+'.txt')
dy =df1
#df2= np.genfromtxt(r'C:\Users\icky\Desktop\Philips\02TestIsc\siftxt/'+Yr+doy+'.txt')*0.001
df2= np.genfromtxt(r'C:\Users\eomf\Desktop\siftxt/'+Yr+doy+'.txt') 
dx=df2

#判断2个矩阵中的空值，并去除
bad = ~np.logical_or(np.isnan(dx), np.isnan(dy))
dx1=np.compress(bad, dx)  #compress：按照给定的bool list来选取ndarray中的值, 返回一个新的 ndarray
dy1=np.compress(bad, dy)  

#计算皮尔逊相关系数和P值
corr, pvalue=stats.pearsonr(dx1, dy1)
            
#排序，为二项式绘图作准备，
dataset = pd.DataFrame(list(zip(dx1,dy1)))
dataset = dataset.sort_values(0)
dx1=dataset[0].values
dy1=dataset[1].values
            
            
xy = np.vstack([dx1,dy1])#按垂直方向（行顺序）堆叠数组构成一个新的数组
#高斯核的核密度
z = gaussian_kde(xy)(xy)
idx = z.argsort()
x, y, z = dx1[idx], dy1[idx], z[idx]

fig, ax = plt.subplots()
#绘制核密度图
ax.scatter(x, y, c=z, s=30, edgecolor='')
        
            # calc the linefit trendline
            # linefit = np.polyfit(dx1, dy1, 1)
            # y = linefit[0] * dx1 +linefit[1]
            # ax.plot(dx1, y, color='b')
#计算拟合函数        
# calc the polynomial trend
#转成列矩阵
x  = dx1.reshape(-1,1)
y  = dy1.reshape(-1,1)

polynomial_features_1= PolynomialFeatures(degree=1)#degree几次方程，默认是2
xp1 = polynomial_features_1.fit_transform(x)
model1 = sm.OLS(y, xp1).fit()
ypred = model1.predict(xp1)
ax.plot(x,ypred,linewidth=2,color='r')

##线性拟合的参数获取
model1.summary()#总的结果参数
model1.params#常数，和斜率
model1.rsquared#r2
model1.bse#standard error（常数，和斜率）
model1.pvalues#pvalue（常数，和斜率）

#统一设置X和Y轴的标签参数
ax.tick_params(axis='both', labelsize=6, direction='in', bottom=True, length=2, width=1, pad= 3)#which='major',
            
ax.text(0.2, 0.9,"r: %.2f"%corr, fontsize=9, ha='center', va='center', transform=ax.transAxes)
fig.text(0.5, 0.01, 'SIF0.2°_2018', ha='center',fontsize=16,fontweight='bold')
fig.text(0.005, 0.5, 'GPPvpm', va='center', rotation='vertical',fontsize=16,fontweight='bold')
