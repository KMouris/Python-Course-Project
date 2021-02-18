from data_management import *
from check_functions import *
from log import *


def create_lists():
    list1 = []
    list2 = []
    list3 = []
    return list1, list2, list3


def append2list(list1, list2, list3, object1, object2, object3):
    list1.append(object1)
    list2.append(object2)
    list3.append(object3)
    return list1, list2, list3


def get_path_from_list(list1_object, list2_object):
    """

    :param list1_object: Indexed STR Object from LIST
    :param list2_object: Indexed STR Object from LIST
    :return:
    """
    try:
        path1 = list1_object
        path2 = list2_object
    except IndexError as e:  # better to do it with a check function and not in the main code
        logger.error('IndexError: Check the number of files in the input folders')
        print(e)
        sys.exit(1)  # code shouldn't run any further if this error occurs
    return path1, path2


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
def calc_snowdepth(snow_at_start, measured_snow_next_period, satellite_data):
    """
    Calculate snow depth which melts, snow depth at the start and at the end of a period
    :param snow_at_start: ARRAY of actual snow depth at the beginning of a period
    :param measured_snow_next_period: ARRAY of measured snow depths
    :param satellite_data: ARRAY of snow cover
    :return: ARRAY of actual snow depth at the end of a period
             ARRAY of melting snow depth
             ARRAY of actual snow depth at the beginning of the following period
    """
    try:
        calc_snow = RasterCalculations(snow_start_of_period=snow_at_start,
                                       snow_cover=satellite_data,
                                       snow_measured=measured_snow_next_period)
        snow_at_end_array = calc_snow.snow_at_end()
        snowmelt_array = calc_snow.snowmelt(snow_end_of_period=snow_at_end_array)
        snow_start_array = calc_snow.snow_at_start(snow_end_of_period=snow_at_end_array)
        return snow_at_end_array, snowmelt_array, snow_start_array
    except TypeError:
        print("Input arguments have to be ARRAYS.")


@wrap(entering, exiting)
def check_data(array_one, array_two, path_raster_one, path_raster_two, object_one, object_two):
    """
    Compare size of arrays, geotransformation and projection of rasters and number of items in an object
    :param array_one: ARRAY one
    :param array_two: ARRAY two
    :param path_raster_one: STR of raster path one
    :param path_raster_two: STR of raster path two
    :param object_one: object one where len() can be applied, e.g. LIST, TUPLE, STR, etc.
    :param object_two: object two where len() can be applied, e.g. LIST, TUPLE, STR, etc.
    """
    check = CompareData(array_one=array_one, array_two=array_two, raster_one_path=path_raster_one,
                        raster_two_path=path_raster_two)
    check.compare_shape()
    check.compare_projection()
    check.compare_geotransform()
    check.number_of_items(object_one, object_two)


def compare_date(path_raster_one, path_raster_two, filename_one, filename_two):
    """
    Extract the date from the filename of two rasters and compare them.
    :param path_raster_one: STR of raster path one
    :param path_raster_two: STR of raster path two
    :param filename_one: STR of filename one
    :param filename_two: STR of filename two
    """
    manage_raster_one = DataManagement(path=path_raster_one, filename=filename_one)
    manage_raster_two = DataManagement(path=path_raster_two, filename=filename_two)
    if not manage_raster_one.get_date() == manage_raster_two.get_date():
        logger.warning("Rasters have different dates.")
