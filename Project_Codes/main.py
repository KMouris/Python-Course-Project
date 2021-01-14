import os
from raster_calculations import *
from data_management import *
import glob
import time
import sys
sys.path.append(
    r'' + os.path.abspath('../geo-utils/'))  #Of course: replace "D:/Target/Directory/", e.g., with  r'' + os.path.abspath('')
import geo_utils as gu

start_time = time.time()

# User Input
# Folder with snow values
Snow_mm_path = r'' + os.path.abspath('../Input_Data/Snow_per_month/')
# Folder with satellite data
SnowCover_path = r'' + os.path.abspath('../Input_Data/SnowCover/')
# Folder for the results
path_results = r"C:\Users\there\Documents\Python\Python-Course-Project\Results\\"  # r' + os.path.abspath('..\Results\\')

def main():
    # define variables as global
    global sm_year, sm_month, gt, proj
    # Create folder if it does not already exist
    RasterManagement.folder_creation(path_results)
    # Get all file paths into a list: All rasters MUST BE .tif files. if not, the type of file must also be changed.
    snow_mm_paths = sorted(glob.glob(Snow_mm_path + "\\*.tif"))
    snow_cover_paths = sorted(glob.glob(SnowCover_path + "\\*.tif"))
    # Create Lists
    date = []
    snow_mm = []
    snow_cover = []

    # loop trough every snow_mm file
    i = 0
    for file in snow_mm_paths:
        snow_mm_filenames = snow_mm_paths[i]
        snow_cover_filenames = snow_cover_paths[i]
        sm_month, sm_year = RasterManagement.get_date(1, snow_mm_filenames)  # static method or rather just a function
        print(sm_month, sm_year)
        datatype, snow_array, geotransform = gu.raster2array(
            snow_mm_filenames)  # geoutils is maybe the more elegant solution bot no classes
        datatype2, snow_cover_array, geotransform2 = gu.raster2array(
            snow_cover_filenames)
        # write all files in lists
        date.append([sm_month, sm_year])
        snow_mm.append(snow_array)
        snow_cover.append(snow_cover_array)
        # get projection and geotransformation
        gt, proj = RasterManagement.get_raster_data(1, file)
        i += 1  # add to date (row) counter

    # Test Calculation
    result = snow_mm[1] * snow_cover[1]
    save_path = path_results + "Test" + ".tif"  # Assign raster pth, including name and extension
    RasterManagement.save_raster(1, result, save_path, gt, proj)  # Save array as raster
    print(result)
    print('Total time: ', time.time() - start_time, 'seconds')
    pass


    # Test Calculation CLass
    test_end = RasterCalculations.snow_at_end(1, snow_mm[0], snow_cover[0])
    print(test_end)
    save_path = path_results + "Test_end_of_month" + ".tif"
    RasterManagement.save_raster(1, test_end, save_path, gt, proj)

    test_melt = RasterCalculations.snowmelt(1, test_end, snow_mm[0])
    print(test_melt)
    save_path = path_results + "Test_melt" + ".tif"
    RasterManagement.save_raster(1, test_melt, save_path, gt, proj)

    test_start = RasterCalculations.snow_at_start(1, snow_mm[1], test_end)
    print(test_start)
    save_path = path_results + "Test_start" + ".tif"
    RasterManagement.save_raster(1, test_start, save_path, gt, proj)


    # Calculations Loop
    snow_start_of_month = snow_mm
    for i in snow_mm:
      snow_end_of_month = RasterCalculations.snow_at_end(1, snow_start_of_month, snow_cover)
      snow_melt = RasterCalculations.snowmelt(1,snow_end_of_month, snow_mm)
      snow_start_of_month = RasterCalculations.snow_at_start(1,snow_mm[i+1], snow_end_of_month)    # snow_mm[i+1]


if __name__ == '__main__':
    main()