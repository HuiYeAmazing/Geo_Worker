# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 16:30:42 2019

@author: admin
"""

"""
Copyright (C) 2014-2018 The HDF Group
Copyright (C) 2014 John Evans

This example code illustrates how to access and visualize a LAADS MOD08_D3 v6
HDF-EOS2 Grid file in Python.

If you have any questions, suggestions, or comments on this example, please use
the HDF-EOS Forum (http://hdfeos.org/forums).  If you would like to see an
example of any other NASA HDF/HDF-EOS data product that is not listed in the
HDF-EOS Comprehensive Examples page (http://hdfeos.org/zoo), feel free to
contact us at eoshelp@hdfgroup.org or post it at the HDF-EOS Forum
(http://hdfeos.org/forums).

Usage:  save this script and run

    $python MOD08_D3.A2010001.006.2015041224130.hdf.py

The HDF-EOS2 file must be in your current working directory.

Tested under: Python 2.7.14 :: Anaconda custom (64-bit)
Last updated: 2018-02-16
"""
import os
#import matplotlib as mpl
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import numpy as np
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
FILE_NAME = 'D:/f_work/E_public/E1_wangwei/data/MOD16A2/MOD16A2.A2001009.h28v06.006.2017068170401.hdf'


from pyhdf.SD import SD, SDC
#from pyhdf.SD import SD, SDC
hdf = SD(FILE_NAME, SDC.READ)

 # Get global attribute dictionnary
attr = hdf.attributes(full=1)
# Get dataset dictionnary
tables = hdf.datasets()
DATAFIELD_NAME = tuple(tables.keys())[0]
# Read dataset.
data_raw = hdf.select(DATAFIELD_NAME)
data = data_raw[:,:].astype(np.double)

# Read lat/lon.
xdim = hdf.select('XDim')
lon = xdim[:].astype(np.double)

ydim = hdf.select('YDim')
lat = ydim[:].astype(np.double)

# Retrieve attributes.
attrs = data_raw.attributes(full=1)
lna=attrs["long_name"]
long_name = lna[0]
aoa=attrs["add_offset"]
add_offset = aoa[0]
fva=attrs["_FillValue"]
_FillValue = fva[0]
sfa=attrs["scale_factor"]
scale_factor = sfa[0]        
ua=attrs["units"]
units = ua[0]

# Retrieve dimension name.
dim = data_raw.dim(0)
dimname = dim.info()[0]

data[data == _FillValue] = np.nan
data =  scale_factor * (data - add_offset) 
datam = np.ma.masked_array(data, np.isnan(data))

# Use Geographic projection.
ax = plt.axes(projection=ccrs.PlateCarree())

# Plot on map.
p = plt.pcolormesh(lon, lat, datam, transform=ccrs.PlateCarree())

# Put coast lines.
ax.coastlines()

# Put grids.
gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True)

# Put grid labels only at left and bottom.
gl.xlabels_top = False
gl.ylabels_right = False

# Put degree N/E label.
gl.xformatter = LONGITUDE_FORMATTER
gl.yformatter = LATITUDE_FORMATTER

# Adjust colorbar size and location using fraction and pad.
cb = plt.colorbar(p, fraction=0.022, pad=0.01)
cb.set_label(units, fontsize=8)

# Put title.
basename = os.path.basename(FILE_NAME)
plt.title('{0}\n{1}'.format(basename, long_name), fontsize=8)
fig = plt.gcf()

# Save image.
pngfile = "{0}.py.png".format(basename)
fig.savefig(pngfile)
    
#×
#拖拽到此处
#图片将完成下载