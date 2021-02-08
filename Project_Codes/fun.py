from raster_calculations import *
from data_management import *
from check_functions import *
from log import *


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


@wrap(entering, exiting)
def calculate_snowmelt(initial_snow, list_measured_snow, list_satellite_data):
    """
    Calculate snow depth transferred into next month and snow depth which melts by looping through lists of snow data
    :param initial_snow: ARRAY of starting value of snow depth
    :param list_measured_snow: LIST of arrays of measured snow depth
    :param list_satellite_data: LIST of arrays of snow cover
    :return: LIST with arrays of transferred snow depth
             LIST with arrays of melting snow depth
    """
    # Creating result lists
    snow_end_month = []
    snowmelt = []
    snow_start_month = [initial_snow]
    # loop through monthly entry of lists respecting dependency of monthly start value on values of previous month
    k = 0
    m = 1
    for i in list_measured_snow:
        if k == 0:
            # for the first time step starting value of snow depth has to be set
            calculations_snow = RasterCalculations(snow_start_of_period=initial_snow,
                                                   snow_cover=list_satellite_data[k],
                                                   snow_measured=list_measured_snow[m])
        else:
            # for following time steps snow depth at beginning of month is calculated
            calculations_snow = RasterCalculations(snow_start_of_period=snow_start_month[k],
                                                   snow_cover=list_satellite_data[k],
                                                   snow_measured=list_measured_snow[m])

        snow_end_month_array = calculations_snow.snow_at_end()
        snow_melt_array = calculations_snow.snowmelt(snow_end_of_period=snow_end_month_array)
        snow_end_month.append(snow_end_month_array)
        snowmelt.append(snow_melt_array)
        if k < len(list_measured_snow) - 1:
            snow_start_of_month_array = calculations_snow.snow_at_start(snow_end_of_period=snow_end_month_array)
            snow_start_month.append(snow_start_of_month_array)
        k += 1
        if m < len(list_measured_snow) - 1:
            m += 1
    return snow_end_month, snowmelt


@wrap(entering, exiting)
def check_input(array_one, array_two, path_raster_one, path_raster_two, object_one, object_two):
    """
    Compares size of arrays, geotransformation and projection of rasters and number of items in an object
    :param array_one: ARRAY
    :param array_two: ARRAY
    :param path_raster_one: STR of raster path
    :param path_raster_two: STR of raster path
    :param object_one: object where len() can be applied, e.g. LIST, TUPLE, STR, etc.
    :param object_two: object where len() can be applied, e.g. LIST, TUPLE, STR, etc.
    :return:
    """
    check_data = CheckInputData(array_one=array_one, array_two=array_two, raster_one_path=path_raster_one,
                                raster_two_path=path_raster_two)
    check_data.compare_shape()
    check_data.compare_projection()
    check_data.compare_geotransform()
    check_data.number_of_items(object_one, object_two)


def compare_date(path_raster_one, path_raster_two, filename_one, filename_two):
    manage_raster_one = DataManagement(path=path_raster_one, filename=filename_one)
    manage_raster_two = DataManagement(path=path_raster_two, filename=filename_two)
    if not manage_raster_one.get_date() == manage_raster_two.get_date():
        print("Different dates at same index.")



