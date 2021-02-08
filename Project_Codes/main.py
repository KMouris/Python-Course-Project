from check_functions import *
from statistics import *
from log_test import *
from fun import *

start_time = time.time()


# we can think about shifting the functions to a fun.py or into data management.py?
@wrap(entering, exiting)
def raster2nested_list(list_rasterpaths1, list_rasterpaths2):
    """
    Functions reads an arbitrary number of raster files from 2 different folders.
    Extracts the date and the corresponding raster arrays and saves them into nested lists for further calculations.
    :param list_rasterpaths1: LIST of paths to raster files
    :param list_rasterpaths2: LIST of paths to raster files
    :return:    date_list: LIST which contains the year and month of input raster files
                array_list1: LIST which contains the raster arrays of list_rasterpaths1
                array_list2: LIST which contains the raster arrays of list_rasterpaths2
    """
    # create empty lists
    date_list = []
    array_list1 = []
    array_list2 = []
    # loop trough every file to get the dates and raster arrays
    i = 0
    for file in list_rasterpaths1:
        # get the raster path (STR) from the list_rasterpaths (LIST)
        try:
            filenames1 = list_rasterpaths1[i]
            filenames2 = list_rasterpaths2[i]
        except IndexError as i:  # better to do it with a check function and not in the main code
            print('IndexError: Check the number of files in the input folders')
            print(i)
            sys.exit(1)  # code shouldn't run any further if this error occurs
        # instantiate data management object to use get_date method
        data_manager = DataManagement(path=r'' + os.path.abspath('../Results'), filename=filenames1)
        sm_month, sm_year = data_manager.get_date()
        # use raster2array method to get the arrays from the raster files
        datatype, raster_arrays1, geotransform = gu.raster2array(
            filenames1)
        datatype2, raster_arrays2, geotransform2 = gu.raster2array(
            filenames2)
        # create date string (Format: YY/mm)
        month_year = (str(sm_year) + '_' + str(sm_month))
        # write the dates and the raster arrays into lists
        date_list.append([month_year])
        array_list1.append(raster_arrays1)
        array_list2.append(raster_arrays2)
        i += 1  # add to date (row) counter
    return date_list, array_list1, array_list2


start_time = time.time()

# User Input
# Folder with snow values
Snow_mm_path = r'' + os.path.abspath('../Input_Data/Snow_per_month/')
# Folder with satellite data
SnowCover_path = r'' + os.path.abspath('../Input_Data/SnowCover/')
# Folder for the results
path_results = r'' + os.path.abspath('../Results')


@wrap(entering, exiting)
def main():
    # Get all file paths into a list: All rasters must be .tif files. if not, the type of file must also be changed.
    snow_mm_paths = sorted(glob.glob(Snow_mm_path + "\\*.tif"))
    snow_cover_paths = sorted(glob.glob(SnowCover_path + "\\*.tif"))
    # Create folder if it does not already exist
    data_manager = DataManagement(path=path_results, filename=snow_mm_paths[0])
    data_manager.folder_creation()

    # loop trough input rasters, write raster arrays and corresponding dates in nested lists
    date, snow_mm, snow_cover = raster2nested_list(snow_mm_paths, snow_cover_paths)

    # get projection and geotransformation of input raster
    gt, proj = data_manager.get_proj_data()

    # Check Data
    j = 0
    for file in snow_mm:
        check_data = CheckInputData(array_one=snow_mm[j], array_two=snow_cover[j],
                                    raster_one_path=snow_mm_paths[j], raster_two_path=snow_cover_paths[j], datatype='float64')
        check_data.compare_shape()
        check_data.compare_projection()
        check_data.compare_geotransform()
        j += 1

    check_data.number_of_items(snow_mm, snow_cover)

    # Calculations
    snow_end_month, snowmelt = calculate_snowmelt(snow_mm[0], snow_mm, snow_cover)

    # Saving arrays as raster
    k = 0
    for entry in snowmelt:
        save_path = r'' + os.path.abspath('../Results/Snow_end_month') + "/snow_end_month" + str(
            date[k][0]) + ".tif"
        DataManagement.save_raster(save_path, snow_end_month[k], gt, proj)
        save_path = r'' + os.path.abspath('../Results/Snowmelt') + "/snowmelt" + str(
            date[k][0]).strip() + ".tif"
        DataManagement.save_raster(save_path, snowmelt[k], gt, proj)
        k += 1

    # Calculate Statistics (first idea, we could also write a table with statistic summary)
    raster_file = r'' + os.path.abspath('../Results/Snow_end_month/snow_end_month18_2.tif')
    shape_zone = r'' + os.path.abspath('../Input_Data/Shape_files/catchment_kokel.shp')
    get_zon_statistics(raster_file, shape_zone)

    print('Total time: ', time.time() - start_time, 'seconds')


if __name__ == '__main__':
    main()
