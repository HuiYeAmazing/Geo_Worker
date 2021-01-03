# -*- coding: utf-8 -*-
import arcpy,os
import arcpy.mapping as mapping
from arcpy import env
from glob import glob as glb
from arcpy.sa import *

# input dirs
fpath = 'C:/2018年动态监测成果江西省/江西省'
dir_mxd = r'D:\TDLY_JXTJ'
country_dir = u"C:\\2018年动态监测成果江西省\江西省\缓冲区\各县市缓冲区"
# output dirs ----------------------------------------------------
mxds_dir = r'D:\TDLY_JXTJ\OutFiles\MXDS'                                  #<<<<<<<<<<<<<<<<<<<<<<<<<<<出图位置
# shp_dir = 'D:\TDLY_JXTJ\OutFiles\jx_qinshi_rasters'
# if not os.path.exists(shp_dir):
#     os.makedirs(shp_dir)
# -----------------------------------------------------
env.workspace = mxds_dir
env.overwriteOutput = True
region_list1 = ['国家级监测区域', '省级监测区域']
region_list2 = ['一般监测区域', '重点监测区域']
dest_dir_name = '土地利用'

fpath = unicode(fpath, 'utf-8')
region_list1 = [unicode(x, 'utf-8') for x in region_list1]
region_list2 = [unicode(x, 'utf-8') for x in region_list2]
dest_dir_name = unicode(dest_dir_name, 'utf-8')

fmxd1 = dir_mxd + os.sep + u'九江_shp_v.mxd'
fmxd2 = dir_mxd + os.sep + u'九江_shp_h.mxd'

shp_dirs = []
for r1 in region_list1:
    for r2 in region_list2:
        temp_path = os.path.join(fpath, r1, r2)
        county_list = os.listdir(temp_path)
        shp_dirs.append([os.path.join(temp_path, county, dest_dir_name) for county in county_list])

arcpy.CheckOutExtension("Spatial")
for list_dir in shp_dirs:
    for shp_dir in list_dir:
        f_shp = glb(shp_dir + os.sep + '*.shp')[0]
        fstrs = os.path.basename(f_shp).split('.')[0]
        fname = f_shp.split(os.sep)[3]
        region = f_shp.split(os.sep)[1]
        # raster_f = arcpy.Raster(f_raster)
        desc = arcpy.Describe(f_shp)
        data_extent = [desc.extent.XMin, desc.extent.XMax, desc.extent.YMin, desc.extent.YMax]
        if (data_extent[1] - data_extent[0]) > (data_extent[3] - data_extent[2]):
            fmxd = fmxd1
        else:
            fmxd = fmxd2
        print(fname)
        # =============================== 重分类 ===========================
        out_fmxd = mxds_dir + os.sep + fname + ".mxd"  # 绝对路径+文件名+后缀
        # outReclassTif = shp_dir + os.sep + fname + ".tif"
        # read standard mxd file ======----------------------
        mxd = mapping.MapDocument(fmxd)
        df = mapping.ListDataFrames(mxd)[0]
        layers = mapping.ListLayers(mxd, "", df)
        # 先查找样例图中的相关图层

        TiffLyr = layers[2]
        shpLyr = layers[0]
                # print("找到边界！")
            # if lyr.name == u'崇义县_Buffer':
            #     bufferLyr = lyr
            #     print("找到2！")
            #     continue
        # == == == -------------------------------------------
        # 开始ReplaceDataSource
        # ===============================参数设置=========================
        # 输入设置：输入tif、边界shp、buffershp
        # newTiffName = fname + ".tif"   # 新栅格文件名，带后缀
        newShpPath = country_dir + os.sep + fname  # 上次创建好了的BUFFERS_Coding\县名
        newShpName = fname  # + r".shp"
        # newBufferName = newCityName + "_buffer_500M"   # r"_buffer_500M.shp"
        # 输出设置：保存mxd
        # =============================== 替换 ===========================
        try:
            shpLyr.replaceDataSource(newShpPath, "SHAPEFILE_WORKSPACE", newShpName)
        except:
            print(fname + " shape file not exist.")
            continue
        TiffLyr.replaceDataSource(shp_dir, "SHAPEFILE_WORKSPACE", fstrs)
             # newShpName不带后缀
        #bufferLyr.replaceDataSource(newShpPath, "SHAPEFILE_WORKSPACE", newBufferName)
        mxd.saveACopy(out_fmxd)    # 将替换后的mxd保存至outfPath
        # ========================= 开始设置输出元素 ======================
        # 先读取上面保存的mxd初始化为mxd2
        mxd_ = mapping.MapDocument(mxds_dir + os.sep + fname + ".mxd")
        df_mxd = mapping.ListDataFrames(mxd_)[0]
        TiffLyr = arcpy.mapping.ListLayers(mxd_, "", df_mxd)[2]
        # 设置比例尺
        df_mxd.extent = TiffLyr.getExtent()    # 缩放至图层
        txtElm = mapping.ListLayoutElements(mxd_, "DATAFRAME_ELEMENT")[0]
        df_mxd.scale = int(txtElm.scale * 0.0001) * 10000
        # df.scale = 1875523   #1：1875523
        # 设置title
        # mxd2.title = newCityName + u"土壤侵蚀分布图"
        arcpy.RefreshActiveView()  # 刷新地图和布局窗口
        arcpy.RefreshTOC()         # 刷新内容列表
        mxd_.save()    # 将替换后的mxd保存至outfPath
        out_tiff = dir_mxd + os.sep + 'OutFiles\\TIFS' + os.sep + fname + '_土地利用.tif'
        mapping.ExportToTIFF(mxd_, out_tiff=out_tiff, resolution=300)
        # arcpy.mapping.ExportToPNG(mxd_, dir_mxd + os.sep + fname +u'侵蚀.png')
        print(fname + "output OK")
