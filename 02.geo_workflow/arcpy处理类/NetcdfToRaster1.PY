# This script is used to convert Netcdf dataset To Raster.
# Edit by HuiYe 2015/04/01
# INPUT FILE: inMaskData
# Import system modules
import arcgisscripting, sys, string, os, math, arcpy
from arcpy import env
from arcpy.sa import *

# Create the Geoprocessor object
# gp = arcgisscripting.create()

iway = "D:/f_work/E_public/E5_wxx"
oway = iway + os.sep + 'NC_spei'

# Name: MakeNetCDFRasterLayer_Ex_02.py
# Description: Create a raster layer from a netCDF file.
# Requirements: None

# Import system modules
# import arcpy, time
yr1 = 1951
yr2 = 1951

# Set local variables
variable = "precip"
XDimension = "longitude"
YDimension = "latitude"
# outRasterLayer = "%s/iAPHRO%d" % (oway, i)
bandDimmension = ""
dimension = "time" 
valueSelectionMethod = "BY_VALUE"

# path = oway

title = "FLOAT_" + variable 
outPath = os.path.join(oway, title)
if not os.path.isdir(outPath):

    os.makedirs(outPath)
# 判断目标目录是否有文件存在			
if os.path.isfile(outPath):
	# 改变当前工作路径
	os.chdir(outPath)
	# 列出所有文件
	ilist = os.listdir(outPath)
	for file in ilist:
		print file
		os.remove(file)

for yr in range(yr1,yr2+1):
	# Input Flie 根据文件名修改
	inNetCDFFile = iway + "\\APHRO_RU_025deg_V1101." + str(yr) + ".nc" 
	# Display properties of NetCDF file
	ncFP = arcpy.NetCDFFileProperties(inNetCDFFile)
	#Get Dimensions
	ncDims = ncFP.getDimensions()
	for dimension in ncDims:

		top = ncFP.getDimensionSize(dimension)
		for i in range(0, top):

			if dimension == "time":

				dimension_values = ncFP.getDimensionValue(dimension, i)
				# print dimension_values
				date = dimension_values.split("/")
				yr  = date[0]
				mn  = date[1]
				doy = date[2]
				YMD = int(yr) * 10000 + int(mn) * 100 + int(doy)
				nowFile = str(YMD) 
				element = "APHRO" + nowFile
				outRasterLayer = oway + "\\APHRO" + nowFile

				#THIS IS THE NEW CODE HERE
				dv1 = ["time", dimension_values]
				dimension_values = [dv1]
				
				env.workspace = oway
				if arcpy.Exists(element):
					# Execute Delete
					arcpy.Delete_management(element, "")
				# print nowFile
				#END NEW CODE
				# Execute MakeNetCDFRasterLayer
				# Confirm that the feature class exists
				#				
				arcpy.MakeNetCDFRasterLayer_md(inNetCDFFile, variable, XDimension, YDimension, nowFile, bandDimmension, dimension_values, valueSelectionMethod)
				arcpy.CopyRaster_management(nowFile, outRasterLayer, "", "", "", "NONE", "NONE", "")
				
				# Description: Extracts the cells of a raster that correspond with the areas
				#    defined by a mask.
				# Requirements: Spatial Analyst Extension
				# Set environment settings
				env.workspace = oway
				inMaskData = "Z:\\YeHui_Zone\\Paper\\Database\\Boundary\\zone_84"
				# Set local variables
				inRaster = element
				
				# Check out the ArcGIS Spatial Analyst extension license
				arcpy.CheckOutExtension("Spatial")

				# Execute ExtractByMask
				outExtractByMask = ExtractByMask(inRaster, inMaskData)

				# Save the output 
				outExtractRaster = "CA" + nowFile
				if arcpy.Exists(outExtractRaster):
					# Execute Delete
					arcpy.Delete_management(outExtractRaster, "")
				outExtractByMask.save("CA" + nowFile)
				
				# Description: Converts a raster dataset to a file of binary floating-point
				#     values representing raster data.
				# Requirements: None
							
				print outExtractRaster
				outFloat = outPath + "\\" + outExtractRaster + ".flt"
				# Execute RasterToFloat
				
				arcpy.RasterToFloat_conversion(outExtractRaster, outFloat)

																	  
