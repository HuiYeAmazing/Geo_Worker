# -*- coding: utf-8 -*-

# @author: HuiYe

# Created by Hui Ye on 2017-3-29 16:11
#import arcgisscripting
#import sys
#import string
import os, glob
#import math
import arcpy
from arcpy import env
from glob import glob as glb
from arcpy.sa import *
# from shutil import copyfile
os.system("cls")
arcpy.CheckOutExtension("Spatial")

# FltDir = r'Z:\Database\Meteo1km\MeteoGrid'
FltDir = r'Z:\Database\Meto_1km\China'
ShpDir = r'D:\OneDrive\WorkSpace\Sites'
# HdrDir = r'E:\OneDrive\DataBase\GeoDatabase_HuiYe\Project2File'
TableDir = r'F:\Hui_Zone\Temp\tables'

# HdrName = HdrDir +'\Glopen_China8km_Albers_v110.hdr'
# PrjName = HdrDir + '\WGS84_Albers_v110.prj'

Shps = ['sites_albers110.shp', 'sites_clark.shp']
# vars = ['C8days', 'TEM', 'SSD']
# vars = ['TEM', 'SSD']
vars = ['PRCP', 'TAVG', 'SSD']
# wks = FltDir + '\\temp'
if not os.path.exists(TableDir):
    os.mkdir(TableDir)
# Check out the ArcGIS Spatial Analyst extension license
arcpy.CheckOutExtension("Spatial")
env.overwriteOutput = True
sampMethod = "NEAREST"

yrs = range(2000, 2015 + 1)

for var in vars:
    rstDir = FltDir + os.sep + var
    env.workspace = rstDir
    if var == 'C8days':
        ShpFile = ShpDir + os.sep + Shps[1]
    else:
        ShpFile = ShpDir + os.sep + Shps[0]
    # tabels = []
    # i = 1
    for yr in yrs:
        fname = '*' + str(yr) + '*.flt'
        # rasts = sorted(glb(fname))
        rasters = arcpy.ListRasters(fname, 'FLT')
        if rasters:
            if var == 'TAVG':
                Table = TableDir + os.sep + 'TEM' + str(yr)
            else:
                Table = TableDir + os.sep + var + str(yr)
            # for raster in rasters:
            #     rst = arcpy.Raster(raster)
            #     fltname = raster[:-4]
            #     strname = os.path.basename(raster)[:-4]
            print Table
            # HdrFile = fltname + '.hdr'
            # PrjFile = fltname + '.prj'
            # # HdrName = FltFile + '*.hdr'
            # if not os.path.exists(HdrFile):
            #     copyfile(HdrName, HdrFile)
            # if not os.path.exists(PrjFile):
            #     copyfile(PrjName, PrjFile)

            Sample(rasters, ShpFile, Table, sampMethod)
            arcpy.TableToDBASE_conversion(Table, TableDir)
            arcpy.Delete_management(Table)
            # outTable = TableDir + Var + str(yr)
            # ID = yr * 100 + i
            # i = i + 1

            # Execute Sample




