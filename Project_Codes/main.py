import os
from raster_calculations import *
from data_management import *
import glob
import time
import sys

sys.path.append(
    r'' + os.path.abspath(
        '../geo-utils/'))  # Of course: replace "D:/Target/Directory/", e.g., with  r'' + os.path.abspath('')
import geo_utils as gu

start_time = time.time()

# User Input
# Folder with snow values
Snow_mm_path = r'' + os.path.abspath('../Input_Data/Snow_per_month/')
# Folder with satellite data
SnowCover_path = r'' + os.path.abspath('../Input_Data/SnowCover/')

# Folder for the results
path_results = r'' + os.path.abspath('../Results')
# path_results = r"C:\Users\Mouris\Desktop\Python\Python_Sebastian\Python-Course-Project\Results\\"
# path_results = r"C:\Users\there\Documents\Python\Python-Course-Project\Results\\"
# ich habe den Ordner leider nicht unter Documents sonst könnte die Variante auch funktionieren


def main():
    # define variables as global
    global sm_year, sm_month, gt, proj
    # Create folder if it does not already exist
    RasterManagement.folder_creation(path_results)
    # Get all file paths into a list: All rasters MUST BE .tif files. if not, the type of file must also be changed.
    snow_mm_paths = sorted(glob.glob(Snow_mm_path + "\\*.tif"))
    snow_cover_paths = sorted(glob.glob(SnowCover_path + "\\*.tif"))

    # Create Input Lists
    date = []
    snow_mm = []
    snow_cover = []

    # Create Result Lists
    snow_end_month = []
    snowmelt = []

    # loop trough input data to save the arrays in nested lists
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

    # Calculations
    k = 0
    initial_snow = snow_mm[0]
    snow_start_month = [initial_snow]  # there's no already existing snow at the start of the calculation
    calculations_snow = RasterCalculations(snow_start_of_month=snow_start_month, snow_cover=snow_cover, snow_measured=snow_mm)  # object = instance of class is created
    for arrays in snow_mm:
        print(date[k])
        snow_end_month_array = calculations_snow.snow_at_end(snow_start_month[k], snow_cover[k])
        snow_melt_array = calculations_snow.snowmelt(snow_end_month_array, snow_mm[k])
        snow_end_month.append(snow_end_month_array)
        snowmelt.append(snow_melt_array)
        if k < len(snow_mm) - 1:  # avoid index error, no calculation for a new month without measurements
            snow_start_of_month_array = calculations_snow.snow_at_start(snow_mm[k + 1], snow_end_month[k])
            snow_start_month.append(snow_start_of_month_array)
        # lists are maybe not needed, they are useful if we want to write only one file
        save_path = r'' + os.path.abspath('../Results/Snow_end_month') + "/snow_end_month" + str(
            date[k]) + ".tif"
        RasterManagement.save_raster(1, snow_end_month[k], save_path, gt, proj)
        save_path = r'' + os.path.abspath('../Results/Snowmelt') + "/snowmelt" + str(
            date[k]) + ".tif"
        RasterManagement.save_raster(1, snowmelt[k], save_path, gt, proj)
        k += 1

    print('Total time: ', time.time() - start_time, 'seconds')


if __name__ == '__main__':
    main()
