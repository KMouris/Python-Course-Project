from statistics import *
from fun import *

start_time = time.time()


@wrap(entering, exiting)
def raster2list(list_rasterpaths1, list_rasterpaths2):
    """
    Functions reads an arbitrary number of raster files from 2 different folders.
    Extracts the date and the corresponding raster arrays and saves them into lists for further calculations.
    :param list_rasterpaths1: LIST of paths to raster files
    :param list_rasterpaths2: LIST of paths to raster files
    :return:    date_list: LIST which contains the year and month of input raster files
                array_list1: LIST which contains the raster arrays of list_rasterpaths1
                array_list2: LIST which contains the raster arrays of list_rasterpaths2
    """
    # create empty lists
    date_list, array_list1, array_list2 = create_lists()
    # loop trough every file to get the dates and raster arrays  # maybe loop in main? But I'm not sure if better rather ineffective
    i = 0
    for file in list_rasterpaths1:
        # get the raster path (STR) from the list_rasterpaths (LIST)
        filenames1, filenames2 = get_path_from_list(list_rasterpaths1[i], list_rasterpaths2[i])
        # create date string (YY/mm)
        data_manager = DataManagement(path=r'' + os.path.abspath('../Results'), filename=filenames1)
        month_year = data_manager.create_date_string()
        # use raster2array method to get the arrays from the raster files
        datatype, raster_arrays1, geotransform = gu.raster2array(
            filenames1)
        datatype2, raster_arrays2, geotransform2 = gu.raster2array(
            filenames2)
        # write the dates and the raster arrays into lists
        date_list, array_list1, array_list2 = append2list(date_list, array_list1, array_list2, [month_year],
                                                          raster_arrays1, raster_arrays2)
        i += 1  # add to date (row) counter
    return date_list, array_list1, array_list2


@wrap(entering, exiting)
def snowcalc_over_list(initial_snow, satellite_data, measured_snow_next_period):
    """

    :param initial_snow: ARRAY
    :param satellite_data: LIST
    :param measured_snow_next_period: LIST
    :return:
    """
    snow_end_month, snow_melt, snow_start_month = create_lists()
    snow_start_month.append(initial_snow)
    k = 0
    m = 1
    try:
        for i in measured_snow_next_period:
            snow_end_array, snowmelt_array, snow_start_array = snowdepth(snow_start_month[k],
                                                                         measured_snow_next_period[m],
                                                                         satellite_data[k])
            snow_end_month.append(snow_end_array)
            snow_melt.append(snowmelt_array)
            if k < len(measured_snow_next_period) - 1:
                snow_start_month.append(snow_start_array)
            k += 1
            if m < len(measured_snow_next_period) - 1:
                m += 1
    except IndexError:
        logger.error("IndexError: Check number of items in list.")
    return snow_end_month, snow_melt


@wrap(entering, exiting)
def main():  # maybe we should modularize it further? shift whole loops? Then we will have no big functions anymore
    # Get all file paths into a list: All rasters must be .tif files. if not, the type of file must also be changed.
    snow_mm_paths = sorted(glob.glob(Snow_mm_path + "\\*.tif"))
    snow_cover_paths = sorted(glob.glob(SnowCover_path + "\\*.tif"))

    # Create folder if it does not already exist
    data_manager = DataManagement(path=path_results, filename=snow_mm_paths[0])
    data_manager.folder_creation()

    # Check dates at same index
    i = 0
    for file in snow_cover_paths:
        compare_date(Snow_mm_path, SnowCover_path, snow_mm_paths[i], snow_cover_paths[i])
        i += 1

    # loop trough input rasters, write raster arrays and corresponding dates in lists
    date, snow_mm, snow_cover = raster2list(snow_mm_paths, snow_cover_paths)

    # get projection and geotransformation of input raster
    gt, proj = data_manager.get_proj_data()

    # Check input data
    j = 0
    for file in snow_mm:
        check_data(snow_mm[j], snow_cover[j], snow_cover_paths[j], snow_cover_paths[j], snow_mm_paths, snow_cover_paths)
        j += 1

    # Calculations
    snow_end_month, snow_melt = snowcalc_over_list(snow_mm[0], snow_cover, snow_mm)

    # Saving arrays as raster
    k = 0
    for entry in snow_melt:
        save_path = r'' + os.path.abspath('../Results/Snow_end_month') + "/snow_end_month" + str(date[k][0]) + ".tif"
        DataManagement.save_raster(save_path, snow_end_month[k], gt, proj)
        save_path = r'' + os.path.abspath('../Results/Snowmelt') + "/snowmelt" + str(date[k][0]) + ".tif"
        DataManagement.save_raster(save_path, snow_melt[k], gt, proj)
        k += 1

    # Calculate and plot zonal statistics
    zonal_statistics = ZonStatistics(path_raster=snow_result_paths, shape=shape_zone, datelist=date)
    zonal_statistics.get_zon_statistic()
    zonal_statistics.plot_zon_statistics()
    print('Total time: ', time.time() - start_time, 'seconds')
    logging.shutdown()


if __name__ == '__main__':
    main()
