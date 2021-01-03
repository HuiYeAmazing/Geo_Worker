# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 17:35:39 2020

@author: eomf
"""

%reset -f
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from scipy import stats
import seaborn as sns

file_dir = r'D:\FD\wetland_classification_1984-2018\Wetland_maps\Area_stat'
#area of mariculture
file_name = 'China_all.csv'
file = os.path.join(file_dir,file_name)

dat = pd.read_csv(file)

dat = dat.iloc[0:31, 0:9]
dat = dat
dat.Year = dat.Year.astype(float)
dat.Wetlands = dat.Wetlands/1000.0
dat.Mudflat = dat.Mudflat/1000.0
dat.Vegetation = dat.Vegetation/1000.0
dat.Saltmarsh = dat.Saltmarsh/1000.0
########################################################first figure
#%matplotlib qt5
sns.set(font='Times New Roman')
fig, axs = plt.subplots(3,2, figsize = (10,10))

###########wetlands
dat1 = dat.iloc[0:24,]
dat2 = dat.iloc[24:31,]

f1 = sns.regplot(x = 'Year', y = 'Wetlands', color = 'tab:red', data= dat1, truncate=True, ax = axs[0,0])
f1 = sns.regplot(x = 'Year', y = 'Wetlands',  color = 'tab:blue',data= dat2, truncate=True, ax = axs[0,0])
f1 = sns.scatterplot(x = 'Year', y = 'Wetlands',  color = 'black',data= dat, ax = axs[0,0])
f1 = sns.lineplot(x = 'Year', y = 'Wetlands',  color = 'black',data= dat, ax = axs[0,0])
axs[0,0].set_xlim(1980,2020)
axs[0,0].axvspan(2011.5,2012.5, alpha=0.3, color='tab:orange')
axs[0,0].set_ylabel("Area ($\mathregular{10^3 km^2}$)", fontsize = 12)
axs[0,0].set_xlabel("")
xtick = [int(i) for i in f1.get_xticks()]
ytick = [int(i) for i in f1.get_yticks()]
axs[0,0].set_xticklabels(xtick, fontsize = 11)
axs[0,0].set_yticklabels(ytick, fontsize = 11)
axs[0,0].text(1990, 7.3, 'Slope = -0.13', color = 'tab:red',fontsize = 11)
axs[0,0].text(1990, 6.8, '$\it{p}$  < 0.01', color = 'tab:red',fontsize = 11)
axs[0,0].text(2011, 9, 'Slope = 0.26', color = 'tab:blue',fontsize = 11)
axs[0,0].text(2011, 8.5, '$\it{p}$  > 0.05', color = 'tab:blue',fontsize = 11)
axs[0,0].text(1981, 10, 'A', color = 'black',fontsize = 13)
###########vegetation
dat1 = dat.iloc[0:24,]
dat2 = dat.iloc[24:31,]

f2 = sns.regplot(x = 'Year', y = 'Vegetation', color = 'tab:red', data= dat1, truncate=True, ax = axs[0,1])
f2 = sns.regplot(x = 'Year', y = 'Vegetation',  color = 'tab:blue',data= dat2, truncate=True, ax = axs[0,1])
f2 = sns.scatterplot(x = 'Year', y = 'Vegetation',  color = 'black',data= dat, ax = axs[0,1])
f2 = sns.lineplot(x = 'Year', y = 'Vegetation',  color = 'black',data= dat, ax = axs[0,1])
axs[0,1].set_xlim(1980,2020)
axs[0,1].axvspan(2011.5,2012.5, alpha=0.3, color='tab:orange')
axs[0,1].set_ylabel("Area ($\mathregular{10^3 km^2}$)", fontsize = 12)
axs[0,1].set_xlabel("")
xtick = [int(i) for i in f2.get_xticks()]
ytick = [np.round(i,1) for i in f2.get_yticks()]
axs[0,1].set_xticklabels(xtick, fontsize = 11)
axs[0,1].set_yticklabels(ytick, fontsize = 11)
axs[0,1].text(1989, 1.8, 'Slope = -0.02', color = 'tab:red',fontsize = 11)
axs[0,1].text(1989, 1.73, '$\it{p}$  < 0.01', color = 'tab:red',fontsize = 11)
axs[0,1].text(2011, 2.3, 'Slope = 0.06', color = 'tab:blue',fontsize = 11)
axs[0,1].text(2011, 2.23, '$\it{p}$  < 0.01', color = 'tab:blue',fontsize = 11)
axs[0,1].text(1981, 2.22, 'B', color = 'black',fontsize = 13)
###########Mangrove
dat1 = dat.iloc[0:12,]
dat2 = dat.iloc[12:31,]

ax = axs[1,0]
f3 = sns.regplot(x = 'Year', y = 'Mangrove', color = 'tab:red', data= dat1, truncate=True, ax = ax)
f3 = sns.regplot(x = 'Year', y = 'Mangrove',  color = 'tab:blue',data= dat2, truncate=True, ax = ax)
f3 = sns.scatterplot(x = 'Year', y = 'Mangrove',  color = 'black',data= dat, ax = ax)
f3 = sns.lineplot(x = 'Year', y = 'Mangrove',  color = 'black',data= dat, ax = ax)
ax.set_xlim(1980,2020)
ax.axvspan(1999.5,2000.5, alpha=0.3, color='tab:brown')
ax.set_ylabel("Area ($\mathregular{km^2}$)", fontsize = 12)
ax.set_xlabel("")
xtick = [int(i) for i in f3.get_xticks()]
ytick = [int(i) for i in f3.get_yticks()]
ax.set_xticklabels(xtick, fontsize = 11)
ax.set_yticklabels(ytick, fontsize = 11)
ax.text(1988, 160, 'Slope = -1', color = 'tab:red',fontsize = 11)
ax.text(1988, 148, '$\it{p}$  > 0.05', color = 'tab:red',fontsize = 11)
ax.text(2010, 160, 'Slope = 4.7', color = 'tab:blue',fontsize = 11)
ax.text(2010, 148, '$\it{p}$  < 0.01', color = 'tab:blue',fontsize = 11)
ax.text(1981, 215, 'C', color = 'black',fontsize = 13)

###########Saltmarsh
dat1 = dat.iloc[0:24,]
dat2 = dat.iloc[24:31,]

ax = axs[1,1]
f4 = sns.regplot(x = 'Year', y = 'Saltmarsh', color = 'tab:red', data= dat1, truncate=True, ax = ax)
f4 = sns.regplot(x = 'Year', y = 'Saltmarsh',  color = 'tab:blue',data= dat2, truncate=True, ax = ax)
f4 = sns.scatterplot(x = 'Year', y = 'Saltmarsh',  color = 'black',data= dat, ax = ax)
f4 = sns.lineplot(x = 'Year', y = 'Saltmarsh',  color = 'black',data= dat, ax = ax)
ax.set_xlim(1980,2020)
ax.axvspan(2011.5,2012.5, alpha=0.3, color='tab:orange')
ax.set_ylabel("Area ($\mathregular{10^3 km^2}$)", fontsize = 12)
ax.set_xlabel("")
xtick = [int(i) for i in f4.get_xticks()]
ytick = [np.round(i,1) for i in f4.get_yticks()]
ax.set_xticklabels(xtick, fontsize = 11)
ax.set_yticklabels(ytick, fontsize = 11)
ax.text(1988, 1.7, 'Slope = -0.03', color = 'tab:red',fontsize = 11)
ax.text(1988, 1.6, '$\it{p}$  < 0.01', color = 'tab:red',fontsize = 11)
ax.text(2011, 2.1, 'Slope = 0.06', color = 'tab:blue',fontsize = 11)
ax.text(2011, 2.00, '$\it{p}$  < 0.01', color = 'tab:blue',fontsize = 11)
ax.text(1981, 2.15, 'D', color = 'black',fontsize = 13)
###########Mudflat
dat1 = dat.iloc[0:24,]
dat2 = dat.iloc[24:31,]

ax = axs[2,0]
f5 = sns.regplot(x = 'Year', y = 'Mudflat', color = 'tab:red', data= dat1, truncate=True, ax = ax)
f5 = sns.regplot(x = 'Year', y = 'Mudflat',  color = 'tab:blue',data= dat2, truncate=True, ax = ax)
f5 = sns.scatterplot(x = 'Year', y = 'Mudflat',  color = 'black',data= dat, ax = ax)
f5 = sns.lineplot(x = 'Year', y = 'Mudflat',  color = 'black',data= dat, ax = ax)
ax.set_xlim(1980,2020)
ax.axvspan(2011.5,2012.5, alpha=0.3, color='tab:orange')
ax.set_ylabel("Area ($\mathregular{10^3 km^2}$)", fontsize = 12)
ax.set_xlabel("Year", fontsize = 12)
xtick = [int(i) for i in f5.get_xticks()]
ytick = [int(i) for i in f5.get_yticks()]
ax.set_xticklabels(xtick, fontsize = 11)
ax.set_yticklabels(ytick, fontsize = 11)
ax.text(1990, 5.5, 'Slope = -0.11', color = 'tab:red',fontsize = 11)
ax.text(1990, 5.0, '$\it{p}$  < 0.01', color = 'tab:red',fontsize = 11)
ax.text(2011, 7, 'Slope = 0.19', color = 'tab:blue',fontsize = 11)
ax.text(2011, 6.5, '$\it{p}$  > 0.05', color = 'tab:blue',fontsize = 11)
ax.text(1981, 8, 'E', color = 'black',fontsize = 13)
###########Normalization
norm_dir = r'D:\FD\wetland_classification_1984-2018\Wetland_maps\DrivingFactors\Multi-regression'
norm_name = 'statis_sum_China_norm.xlsx'
norm_dat = pd.read_excel(os.path.join(norm_dir,norm_name))
norm_dat = norm_dat.iloc[0:31,]
norm_dat.Year = norm_dat.Year.astype(int)

ax = axs[2,1]

f6 = sns.scatterplot(x = 'Year', y = 'NormAA',  color = 'tab:blue',data= norm_dat, ax = ax, label = 'Aquaculture area')
f6 = sns.lineplot(x = 'Year', y = 'NormAA',  color = 'tab:blue',data= norm_dat, ax = ax)
f6 = sns.scatterplot(x = 'Year', y = 'NormPop',  color = 'tab:red',data= norm_dat, ax = ax, label = 'Population')
f6 = sns.lineplot(x = 'Year', y = 'NormPop',  color = 'tab:red',data= norm_dat, ax = ax)
f6 = sns.scatterplot(x = 'Year', y = 'NormGDP',  color = 'tab:green',data= norm_dat, ax = ax, label = 'GDP')
f6 = sns.lineplot(x = 'Year', y = 'NormGDP',  color = 'tab:green',data= norm_dat, ax = ax)
f6 = sns.scatterplot(x = 'Year', y = 'NorNl',  color = 'tab:cyan',data= norm_dat, ax = ax, label = 'Nightlight')
f6 = sns.lineplot(x = 'Year', y = 'NorNl',  color = 'tab:cyan',data= norm_dat, ax = ax)

ax.set_xlim(1980,2020)
ax.axvspan(1999.5,2000.5, alpha=0.3, color='tab:brown')
ax.axvspan(2011.5,2012.5, alpha=0.3, color='tab:orange')
ax.set_ylabel("Normalized statistical values", fontsize = 12)
ax.set_xlabel("Year", fontsize = 12)
xtick = [int(i) for i in f6.get_xticks()]
ytick = [np.round(i,1) for i in f6.get_yticks()]
ax.set_xticklabels(xtick, fontsize = 11)
ax.set_yticklabels(ytick, fontsize = 11)
ax.text(1981,0.9, 'F', color = 'black',fontsize = 13)
ax.legend(loc = 'center left', fontsize = 11)

outpath = r'D:\FD\wetland_classification_1984-2018\Wetland_maps\Area_stat\new_trend_figure_China'
out_name = os.path.join(outpath,'China_trends_seaborn.pdf')
fig.savefig(out_name, dpi = 400, bbox_inches = 'tight')