# -*- coding: utf-8 -*-
import arcpy,os
import arcpy.mapping as mapping
from arcpy import env
from glob import glob as glb
from arcpy.sa import *

# input dirs
fpath = 'C:/2018年动态监测成果江西省/江西省'
dir_mxd = r'D:\Qinshi_JXTJ'
country_dir = u"C:\\2018年动态监测成果江西省\江西省\缓冲区\各县市缓冲区"
# output dirs ----------------------------------------------------
mxds_dir = r'D:\Qinshi_JXTJ\OutFiles\MXDS'
qinshi_raster_dir = 'D:\Qinshi_JXTJ\OutFiles\jx_qinshi_rasters'
if not os.path.exists(qinshi_raster_dir):
    os.makedirs(qinshi_raster_dir)
# -----------------------------------------------------
env.workspace = mxds_dir
env.overwriteOutput = True
region_list1 = ['国家级监测区域', '省级监测区域']
region_list2 = ['一般监测区域', '重点监测区域']
dest_dir_name = ['土壤侵蚀/土壤侵蚀强度', '土壤侵蚀']

fpath = unicode(fpath, 'utf-8')
region_list1 = [unicode(x, 'utf-8') for x in region_list1]
region_list2 = [unicode(x, 'utf-8') for x in region_list2]

fmxd1 = dir_mxd + os.sep + u'崇义_qinshi_v.mxd'
fmxd2 = dir_mxd + os.sep + u'崇义_qinshi_h.mxd'

shp_dirs = []
for r1 in region_list1:
    if r1 == region_list1[1]:
        dest_dir_name_1 = dest_dir_name[0]
    else:
        dest_dir_name_1 = dest_dir_name[1]
    dest_dir_name_1 = unicode(dest_dir_name_1, 'utf-8')
    for r2 in region_list2:
        temp_path = os.path.join(fpath, r1, r2)
        county_list = os.listdir(temp_path)
        shp_dirs.append([os.path.join(temp_path, county, dest_dir_name_1) for county in county_list])

arcpy.CheckOutExtension("Spatial")
for list_dir in shp_dirs:
    for shp_dir in list_dir:
        f_raster = glb(shp_dir + os.sep + '*.tif')[0]
        fname = f_raster.split(os.sep)[3]
        region = f_raster.split(os.sep)[1]
        raster_f = arcpy.Raster(f_raster)
        desc = arcpy.Describe(raster_f)
        # data_extent = [desc.extent.XMin, desc.extent.XMax, desc.extent.YMin, desc.extent.YMax]
        if desc.height > desc.width:
            fmxd = fmxd1
        else:
            fmxd = fmxd2
        print(fname)
        # =============================== 重分类 ===========================
        out_fmxd = mxds_dir + os.sep + fname + ".mxd"  # 绝对路径+文件名+后缀
        outReclassTif = qinshi_raster_dir + os.sep + fname + ".tif"
        if region == u"国家级监测区域":
            raster_tmp = raster_f - 10
            raster_tmp.save(outReclassTif)
            # arcpy.Delete_management(raster_tmp)
        else:
            arcpy.Copy_management(raster_f, outReclassTif)
        # read standard mxd file ======----------------------
        mxd = mapping.MapDocument(fmxd)
        df = mapping.ListDataFrames(mxd)[0]
        layers = mapping.ListLayers(mxd, "", df)
        # 先查找样例图中的相关图层
        for lyr in layers:
            if 'tif' in lyr.name:
                TiffLyr = lyr
                # print("找到tif！")
            if lyr.name == u'崇义县':
                shpLyr = lyr
                # print("找到1！")
            # if lyr.name == u'崇义县_Buffer':
            #    bufferLyr = lyr
            #    print("找到2！")
        # == == == -------------------------------------------
        # 开始ReplaceDataSource
        # ===============================参数设置=========================
        # 输入设置：输入tif、边界shp、buffershp
        newTiffName = fname + ".tif"   # 新栅格文件名，带后缀
        newShpPath = country_dir + os.sep + fname # 上次创建好了的BUFFERS_Coding\县名
        newShpName = fname  # + r".shp"
        # newBufferName = newCityName + "_buffer_500M"   # r"_buffer_500M.shp"
        # 输出设置：保存mxd
        # =============================== 替换 ===========================
        try:
            shpLyr.replaceDataSource(newShpPath, "SHAPEFILE_WORKSPACE", newShpName)
        except:
            print(fname + " shape file not exist.")
            continue
        TiffLyr.replaceDataSource(qinshi_raster_dir, "RASTER_WORKSPACE", newTiffName)
             # newShpName不带后缀
        #bufferLyr.replaceDataSource(newShpPath, "SHAPEFILE_WORKSPACE", newBufferName)

        mxd.saveACopy(out_fmxd)    # 将替换后的mxd保存至outfPath
        # ========================= 开始设置输出元素 ======================
        # 先读取上面保存的mxd初始化为mxd2
        mxd_ = mapping.MapDocument(mxds_dir + os.sep + fname + ".mxd")
        df_mxd = mapping.ListDataFrames(mxd_)[0]
        layers = arcpy.mapping.ListLayers(mxd_, "", df_mxd)
        for lyr in layers:
            if lyr.name == 'QD.tif':
                TiffLyr = lyr
        # 设置比例尺
        df_mxd.extent = TiffLyr.getExtent()    # 缩放至图层
        df_mxd.extent = TiffLyr.getExtent()  # 缩放至图层
        txtElm = mapping.ListLayoutElements(mxd_, "DATAFRAME_ELEMENT")[0]
        df_mxd.scale = int(txtElm.scale * 0.0001) * 10000
        # df.scale = 1875523   #1：1875523
        # 设置title
        # mxd2.title = newCityName + u"土壤侵蚀分布图"
        arcpy.RefreshActiveView()  # 刷新地图和布局窗口
        arcpy.RefreshTOC()         # 刷新内容列表
        mxd_.save()    # 将替换后的mxd保存至outfPath
        out_tiff = dir_mxd + os.sep + 'OutFiles\\TIFS' + os.sep + fname + u'_土壤侵蚀.tif'
        mapping.ExportToTIFF(mxd_, out_tiff=out_tiff, resolution=300)
        # arcpy.mapping.ExportToPNG(mxd2, outDir + os.sep + fname +u'侵蚀.png')
        print(fname + "output OK")
