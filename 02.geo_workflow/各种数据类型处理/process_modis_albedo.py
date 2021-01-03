# -*- coding:utf8 -*-
import os
import subprocess
import glob
import threading
import numpy as np
from osgeo import gdal
import osr


class ProcessRaster(object):
    def read_raster(self, filename):
        dataset = gdal.Open(filename)
        im_geotrans = dataset.GetGeoTransform()
        im_proj = dataset.GetProjection()
        im_data = dataset.ReadAsArray(0, 0, dataset.RasterXSize, dataset.RasterYSize)
        del dataset
        return im_proj, im_geotrans, im_data

    def write_raster(self, filename, im_proj, im_geotrans, im_data):
        # gdal.GDT_Byte,
        # gdal .GDT_UInt16, gdal.GDT_Int16, gdal.GDT_UInt32, gdal.GDT_Int32,
        # gdal.GDT_Float32, gdal.GDT_Float64
        if 'int8' in im_data.dtype.name:
            datatype = gdal.GDT_Byte
        elif 'int16' in im_data.dtype.name:
            datatype = gdal.GDT_UInt16
        else:
            datatype = gdal.GDT_Float32

        if len(im_data.shape) == 3:
            im_bands, im_height, im_width = im_data.shape
        else:
            im_bands, (im_height, im_width) = 1, im_data.shape

        driver = gdal.GetDriverByName("GTiff")
        dataset = driver.Create(filename, im_width, im_height, im_bands, datatype)

        dataset.SetGeoTransform(im_geotrans)
        dataset.SetProjection(im_proj)

        if im_bands == 1:
            dataset.GetRasterBand(1).WriteArray(im_data)
        else:
            for i in range(im_bands):
                dataset.GetRasterBand(i + 1).WriteArray(im_data[i])
        del dataset

def __vegt_cover(NDVI):
    """计算植被覆盖度"""
    mask = np.logical_or(NDVI < 0.125, NDVI>0.8)
    vegt_cover = np.zeros_like(NDVI)
    vegt_cover[~mask] = 1 - np.power((0.8 - NDVI[~mask])/(0.8 - 0.125), 0.7)
    vegt_cover[NDVI < 0.125] = 0.0
    vegt_cover[NDVI > 0.8] = 0.99
    return vegt_cover

def __LAI(NDVI, vegt_cover):
    """Leaf Area Index (LAI)"""

    LAI_1 = np.log(-(vegt_cover - 1)) / -0.45
    LAI_1[LAI_1 > 8] = 8.0
    LAI_2 = (9.519 * np.power(NDVI, 3) + 0.104 * np.power(NDVI, 2) +
             1.236 * NDVI - 0.257)

    LAI = (LAI_1 + LAI_2) / 2.0  # Average LAI
    LAI[LAI < 0.001] = 0.001
    return LAI

def save_lai(NDVI, dst_FilePath, resolution):
    """保存叶面指数"""
    lai, geo, prj = compute_LAI(NDVI, resolution)
    dst_file_name = os.path.split(NDVI)[-1].replace('.hdf', '.tif')
    dst_FileName = os.path.join(dst_FilePath, dst_file_name)
    pr = ProcessRaster()
    pr.write_raster(dst_FileName, prj, geo, lai)
def save_lais(NDVI, dst_FilePath, resolution):
    files = glob.glob(os.path.join(NDVI, '*.hdf'))
    ts = []
    for file in files:
        t = threading.Thread(target=save_lai, args=(file, dst_FilePath, resolution))
        t.start()
        ts.append(t)
    for t in ts:
        t.join()
def compute_LAI(NDVI, resolution):
    """计算叶面指数"""
    band = 0
    epsg_to = "+proj=aea +lat_1=25 +lat_2=47 +lat_0=0 +lon_0=105 +x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs"
    scale_factor = 	0.0001
    NDVI, geo, prj = Open_reprojected_hdf(NDVI, band, epsg_to, scale_factor=scale_factor, res=resolution)
    vegt_cover = __vegt_cover(NDVI)
    LAI = __LAI(NDVI, vegt_cover)
    return LAI, geo, prj

def save_albedo(src_FileName_Refs, dst_FilePath, resolution):
    """保存反照率"""
    albedo, geo, prj = compute_albedo(src_FileName_Refs, resolution)
    dst_file_name = os.path.split(src_FileName_Refs)[-1].replace('.hdf', '.tif')
    dst_FileName = os.path.join(dst_FilePath, dst_file_name)
    pr = ProcessRaster()
    pr.write_raster(dst_FileName, prj, geo, albedo)
def save_albedos(src_FileName_Refs, dst_FilePath, resolution):
    files = glob.glob(os.path.join(src_FileName_Refs, '*.hdf'))
    ts = []
    for file in files:
        t = threading.Thread(target=save_albedo, args=(file, dst_FilePath, resolution))
        t.start()
        ts.append(t)
    for t in ts:
        t.join()
def compute_albedo(src_FileName_Refs, resolution):
    """计算反照率"""
    wave_index = 0  # modis 波段位置
    scale_factor = 0.0001
    epsg_to = "+proj=aea +lat_1=25 +lat_2=47 +lat_0=0 +lon_0=105 +x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs"
    # Calculate the MOD9 based on MODIS by opening and reproject bands

    B1_modis,_,_ = Open_reprojected_hdf(src_FileName_Refs, wave_index + 0, epsg_to, scale_factor, resolution)
    B2_modis,_,_ = Open_reprojected_hdf(src_FileName_Refs, wave_index + 1, epsg_to, scale_factor, resolution)
    B3_modis,_,_ = Open_reprojected_hdf(src_FileName_Refs, wave_index + 2, epsg_to, scale_factor, resolution)
    B4_modis,_,_ = Open_reprojected_hdf(src_FileName_Refs, wave_index + 3, epsg_to, scale_factor, resolution)
    B5_modis,_,_ = Open_reprojected_hdf(src_FileName_Refs, wave_index + 4, epsg_to, scale_factor, resolution)
    B6_modis,_,_ = Open_reprojected_hdf(src_FileName_Refs, wave_index + 5, epsg_to, scale_factor, resolution)
    B7_modis, geo, prj = Open_reprojected_hdf(src_FileName_Refs, wave_index + 6, epsg_to, scale_factor, resolution)

    # Calc surface albedo within shortwave domain using a weighting function (Tasumi et al 2008)
    Surf_albedo = 0.215 * B1_modis + 0.215 * B2_modis + 0.242 * B3_modis + 0.129 * B4_modis + 0.101 * B5_modis + 0.062 * B6_modis + 0.036 * B7_modis
    QC_map = np.zeros_like(Surf_albedo)
    # Define bad pixels
    QC_map[np.logical_or(Surf_albedo < 0.0, Surf_albedo > 1.0)] = 1
    Surf_albedo = np.clip(Surf_albedo, a_min=0, a_max=1)
    return Surf_albedo, geo, prj

def Open_reprojected_hdf(input_names, Band, epsg_to, scale_factor, res):
    """重采样图幅 input_names 可以是list; res：可以是分辨率"""
    if isinstance(input_names, str):
        g = gdal.Open(input_names, gdal.GA_ReadOnly)
        input_name = input_names
        # Open and reproject
        names_in = g.GetSubDatasets()[Band][0]
    else:
        names_in = []
        for input_name in input_names:
            g = gdal.Open(input_name, gdal.GA_ReadOnly)
            name_in = g.GetSubDatasets()[Band][0]
            names_in.append(name_in)
        input_name = input_names[0]

    folder_out = os.path.dirname(input_name)

    output_name_temp = os.path.join(folder_out, "temp_{}.tif".format(os.path.split(os.path.splitext(input_name)[0])[-1]))

    # reproject_MODIS(names_in, output_name_temp, epsg_to)
    # dest, geo, prj = reproject_dataset_res(output_name_temp, res)

    dest, geo, prj = reproject_dataset_res(names_in, res)

    Array = dest.GetRasterBand(1).ReadAsArray() * scale_factor
    try:
        os.remove(output_name_temp)
    except FileNotFoundError:
        pass
    return Array, geo, prj

def reproject_MODIS(input_names, output_name, epsg_to):
    '''
    Reproject the merged data file
    Keywords arguments:
    output_folder -- 'C:/file/to/path/'
    '''
    # Get environmental variable
    # SEBAL_env_paths = os.environ["SEBAL"].split(';')
    # GDAL_env_path = SEBAL_env_paths[0]
    GDAL_env_path = r'.' # gdal的位置需要配置
    GDALWARP_PATH = os.path.join(GDAL_env_path, 'gdalwarp.exe')
    if isinstance(input_names, str):
        split_inputs = input_names.split('hdf":')
        inputname = '%shdf":"%s"' %(split_inputs[0],split_inputs[1])
    else:
        split_inputs = [i.split('hdf":') for i in input_names]
        inputname = ['%shdf":"%s"' % (si[0], si[1].replace('"', '')) for si in split_inputs]
        inputname = ' '.join(inputname)
    # find path to the executable
    fullCmd = ' '.join(["%s" %(GDALWARP_PATH), '-overwrite -s_srs "+proj=sinu +lon_0=0 +x_0=0 +y_0=0 +a=6371007.181 +b=6371007.181 +units=m +no_defs"', '-t_srs "%s" -of GTiff' %(epsg_to), inputname, output_name])
    Run_command_window(fullCmd)

    return()

def reproject_dataset_res(dataset, res, method = 1):
    try:
        if isinstance(dataset, str):
            g_in = gdal.Open(dataset)
        else:
            g_in = dataset
    except:
            g_in = dataset
    epsg_from = get_projection(g_in)

    Geo = g_in.GetGeoTransform()
    X_raster_size = g_in.RasterXSize
    Y_raster_size = g_in.RasterYSize
    ulx = Geo[0]
    uly = Geo[3]
    lrx = ulx + X_raster_size * Geo[1]
    lry = uly + Y_raster_size * Geo[5]

    X_raster_size = int(np.round((lrx - ulx) / res))
    Y_raster_size = int(np.round((uly - lry) / res))
    Geo = list(Geo)
    Geo[1] = res
    Geo[5] = -res
    Geo = tuple(Geo)
    # Set the EPSG codes
    wgs84 = osr.SpatialReference()
    wgs84.ImportFromProj4(epsg_from)

    # Create new raster
    mem_drv = gdal.GetDriverByName("MEM")
    dest1 = mem_drv.Create('', X_raster_size, Y_raster_size, 1, gdal.GDT_Float32)
    dest1.SetGeoTransform(Geo)
    dest1.SetProjection(wgs84.ExportToWkt())

    # Perform the projection/resampling
    if method == 1:
        gdal.ReprojectImage(g_in, dest1, wgs84.ExportToWkt(), wgs84.ExportToWkt(), gdal.GRA_NearestNeighbour)
    elif method == 2:
        gdal.ReprojectImage(g_in, dest1, wgs84.ExportToWkt(), wgs84.ExportToWkt(), gdal.GRA_Average)
    elif method == 3:
        gdal.ReprojectImage(g_in, dest1, wgs84.ExportToWkt(), wgs84.ExportToWkt(), gdal.GRA_Cubic)
    else:
        print('method is None')


    return dest1, Geo, wgs84.ExportToWkt()

def reproject_dataset_example(dataset, dataset_example, method = 1):

    try:
        if (os.path.splitext(dataset)[-1] == '.tif' or os.path.splitext(dataset)[-1] == '.TIF'):
            g_in = gdal.Open(dataset)
        else:
            g_in = dataset
    except:
            g_in = dataset
    epsg_from = get_projection(g_in)

    # open dataset that is used for transforming the dataset
    try:
        if (os.path.splitext(dataset_example)[-1] == '.tif' or os.path.splitext(dataset_example)[-1] == '.TIF'):
            g_ex = gdal.Open(dataset_example)
        else:
            g_ex = dataset_example

    except:
            g_ex = dataset_example
    epsg_to = get_projection(g_ex)

    Y_raster_size = g_ex.RasterYSize
    X_raster_size = g_ex.RasterXSize

    Geo = g_ex.GetGeoTransform()
    ulx = Geo[0]
    uly = Geo[3]
    lrx = ulx + X_raster_size * Geo[1]
    lry = uly + Y_raster_size * Geo[5]

    # Set the EPSG codes
    osng = osr.SpatialReference()
    osng.ImportFromProj4(epsg_to)
    wgs84 = osr.SpatialReference()
    wgs84.ImportFromProj4(epsg_from)

    # Create new raster
    mem_drv = gdal.GetDriverByName('MEM')
    dest1 = mem_drv.Create('', X_raster_size, Y_raster_size, 1, gdal.GDT_Float32)
    dest1.SetGeoTransform(Geo)
    dest1.SetProjection(osng.ExportToWkt())

    # Perform the projection/resampling
    if method == 1:
        gdal.ReprojectImage(g_in, dest1, wgs84.ExportToWkt(), osng.ExportToWkt(), gdal.GRA_NearestNeighbour)
    if method == 2:
        gdal.ReprojectImage(g_in, dest1, wgs84.ExportToWkt(), osng.ExportToWkt(), gdal.GRA_Average)
    if method == 3:
        gdal.ReprojectImage(g_in, dest1, wgs84.ExportToWkt(), osng.ExportToWkt(), gdal.GRA_Cubic)

    return(dest1, ulx, lry, lrx, uly, epsg_to)

def Run_command_window(argument):
    """
    This function runs the argument in the command window without showing cmd window

    Keyword Arguments:
    argument -- string, name of the adf file
    """
    if os.name == 'posix':
        argument = argument.replace(".exe","")
        os.system(argument)

    else:
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        process = subprocess.Popen(argument, startupinfo=startupinfo, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        process.wait()

    return()

def get_projection(g, extension = 'tiff'):
    """
    This function reads the projection of a GEOGCS file or tiff file

    Keyword arguments:
    g -- string
        Filename to the file that must be read
    extension -- tiff or GEOGCS
        Define the extension of the dataset (default is tiff)
    """
    if isinstance(g, str):
        try:
            g = gdal.Open(g)
            print(type(g))
        except:
            print('path is not correct')
    else:
        pass
    # assert isinstance(g ,gdal.Dataset)
    try:
        if extension == 'tiff':
            # Get info of the dataset that is used for transforming
            g_proj = g.GetProjection()
            srs = osr.SpatialReference()
            srs.ImportFromWkt(g_proj)
            epsg_to = srs.ExportToProj4()
        else:
            epsg_to = "+proj=longlat +datum=WGS84 +no_defs"
            print('Was not able to get the projection, so WGS84 is assumed')
    except:
       epsg_to = "+proj=longlat +datum=WGS84 +no_defs"
       print('Was not able to get the projection, so WGS84 is assumed')
    return epsg_to

if __name__ == '__main__':
    src_path = r'D:\SEBAL_Test_Runs\Input\DEM\DEM_CLIP_LS_Clip_Clip11.tif'
    path = r'D:\DEM\NDVI_2019097_h24v04_250.tif'
    ss = r'D:\temp\original\albedo_data\2019113'
    gg = r'D:\temp\standard\albedo_data'
    # reproject_dataset_res(gg, 250)
    save_albedos(ss, gg, 250)

