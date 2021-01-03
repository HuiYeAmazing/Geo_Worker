# -*- coding: utf-8 -*-
"""
Created on Wed Nov  7 22:36:22 2018

@author: Administrator
"""
"""
pymodis.downmodis.downModis(destinationFolder, password=None, user=None, 
                            url='https://e4ftl01.cr.usgs.gov', tiles=None, 
                            path='MOLT', product='MOD11A1.005', today=None, 
                            enddate=None, delta=10, jpg=False, debug=False, 
                            timeout=30, checkgdal=True)
"""
#导入函数库
import os 
from pymodis import downmodis
dest = r"D:\f_work\QingHai_book\MOD13Q1" # This directory for data download
if not os.path.exists(dest): #Test whether a path exists
    os.makedirs(dest)
# Variables for data download
# That's the MODIS tile covering China except the islands in sourth
#tiles = "h23v04, h23v05, h24v04, h24v05, h25v03, h25v04, h25v05, \
#        h25v06, h26v03, h26v04, h26v05,  h26v06,  \
#        h27v04, h27v05, h27v06, h28v05, h28v06, h28v07, h29v06" 
tiles = "h25v05, h26v05" 
product = "MOD13Q1.006"
year = 2000, 2005
for yr in range(year[0], year[1]+1):
    startdate = str(yr) + ".01.01"
    enddate = str(yr) + ".12.31" 
    
    print(str(yr) + ' is downloading !')
    modis_down = downmodis.downModis(destinationFolder=dest, tiles=tiles,
                                     url='https://e4ftl01.cr.usgs.gov',
                                     today=startdate, user = "HuiYe.cn", 
                                     password = "4pgkyr7yXTY4pdg",enddate=enddate, 
                                     product=product,path="MOLT") #MOTA
    modis_down.connect() #Connect to the server and fill the dirData variable
    modis_down.downloadsAllDay() #Download all requested days





