import arcpy, os, math, glob
from arcpy.sa import *
from arcpy import env
env.workspace = r'I:\CentralAsiaNpp20170629\XinJiang\GRID\GLCV'
# InPath = r'F:\luols-data'
outputway = r'I:\CentralAsiaNpp20170629\XinJiang\GRID'
arcpy.CheckOutExtension("Spatial")


# Getting raster properties and writting out the result
f2 = open(outputway + '\\' + 'npp.txt', 'a')
rasterlist = arcpy.ListRasters("*glcv*","grid")
for raster in rasterlist:
	desc = arcpy.Describe(raster)
	name = os.path.basename(raster)
	# name = filename.split('_')[0]
	#Get the geoprocessing result object
	elevSTDResult = arcpy.GetRasterProperties_management(raster, "Mean")
	#Get the elevation standard deviation value from geoprocessing result object
	elevSTD = elevSTDResult.getOutput(0)

	f2.write(str(name) + ',' + elevSTD +'\n')
f2.close()