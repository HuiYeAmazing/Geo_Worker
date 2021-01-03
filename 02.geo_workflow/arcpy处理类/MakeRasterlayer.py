# Import system modules
import arcgisscripting, sys, string, os, math, arcpy

iway = iway = "G:\\迅雷下载\\MOD02QKM"
oway = "E:\\tmp"
outRasterFile = oway + "\\MOD02QKM"
# Try:
arcpy.env.workspace = oway
element = oway + "\\TEMP.TIF"

print "out_rasterlayer1"
arcpy.MakeRasterLayer_management(element, "out_rasterlayer1", "#", "", "1") 
print "out_rasterlayer2"
arcpy.MakeRasterLayer_management(element, "out_rasterlayer2", "#", "", "2")	
# except:
# print "MakeRasterLayer failed."
# print arcpy.GetMessages()
arcpy.CopyRaster_management("out_rasterlayer1",outRasterFile+"B1", "", "", "", "NONE", "NONE", "")
arcpy.CopyRaster_management("out_rasterlayer2",outRasterFile+"B2", "", "", "", "NONE", "NONE", "")
print arcpy.GetMessages()
