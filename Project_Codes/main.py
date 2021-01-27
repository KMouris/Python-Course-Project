try:
    from raster_calculations import *
    from data_management import *
    from check_functions import *
    import sys
    import glob
    import time
    sys.path.append(
        r'' + os.path.abspath(
            '../geo-utils/'))  # Of course: replace "D:/Target/Directory/", e.g., with  r'' + os.path.abspath('')
    import geo_utils as gu

except ModuleNotFoundError as e:
    print('ModuleNotFoundError: Missing fundamental packages (required: sys, glob, time, os, gdal, numpy).')
    print(e)

start_time = time.time()

# User Input
# Folder with snow values
Snow_mm_path = r'' + os.path.abspath('../Input_Data/Snow_per_month/')
# Folder with satellite data
SnowCover_path = r'' + os.path.abspath('../Input_Data/SnowCover/')

# Folder for the results
path_results = r'' + os.path.abspath('../Results')
print(type(path_results))

def main():
    # define variables as global
    global sm_year, sm_month, gt, proj
    # Create folder if it does not already exist
    data_manager = DataManagement(path=path_results, filename='')
    data_manager.folder_creation()
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
        data_manager = DataManagement(path=r'' + os.path.abspath('../Results'), filename=snow_mm_filenames)
        sm_month, sm_year = data_manager.get_date()
        #sm_month, sm_year = DataManagement.get_date(snow_mm_filenames)
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
        print(file)
        gt, proj = data_manager.get_raster_data()
        i += 1  # add to date (row) counter

    # Check Data
    check_data = CheckInputData(array_one=snow_mm, array_two=snow_cover,
                                raster_one_path=snow_mm_paths, raster_two_path=snow_cover_paths)
    check_data.number_of_items(snow_mm, snow_cover)
    j = 0
    for file in snow_mm:
        check_data.compare_shape(snow_mm[j], snow_cover[j])
        check_data.compare_projection(snow_mm_paths[j], snow_cover_paths[j])
        check_data.compare_geotransform(snow_mm_paths[j], snow_cover_paths[j])
        j += 1

    # Calculations
    k = 0
    initial_snow = snow_mm[0]
    snow_start_month = [initial_snow]  # there's no already existing snow at the start of the calculation
    calculations_snow = RasterCalculations(snow_start_of_month=snow_start_month, snow_cover=snow_cover,
                                           snow_measured=snow_mm)  # object = instance of class is created
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
        DataManagement.save_raster(save_path, snow_end_month[k], gt, proj)
        save_path = r'' + os.path.abspath('../Results/Snowmelt') + "/snowmelt" + str(
            date[k]) + ".tif"
        DataManagement.save_raster(save_path, snowmelt[k], gt, proj)
        k += 1

    print('Total time: ', time.time() - start_time, 'seconds')


if __name__ == '__main__':
    main()
