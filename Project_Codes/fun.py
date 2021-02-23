from data_management import *
from raster_calculations import *
from check_functions import *
from log import *


@wrap(entering, exiting)
def snowdepth(snow_at_start, measured_snow_next_period, satellite_data):
    """
    Calculate snow depth which melts, snow depth at the start and at the end of a period
    :param snow_at_start: ARRAY of snow depth at the beginning of a period
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


def create_lists():
    """
    Function which creates three empty lists
    :return:    list1: empty LIST
                list2: empty LIST
                list3: empty LIST
    """
    list1 = []
    list2 = []
    list3 = []
    return list1, list2, list3


def append2list(list1, list2, list3, object1, object2, object3):
    """
    Simple functions which appends objects to lists
    :param list1: LIST before next object is appended
    :param list2: LIST before next object is appended
    :param list3: LIST before next object is appended
    :param object1: LIST, STR, INT, ARRAY... (object which can be appended to a list)
    :param object2: LIST, STR, INT, ARRAY... (object which can be appended to a list)
    :param object3: LIST, STR, INT, ARRAY... (object which can be appended to a list)
    :return:    list1: LIST after object is appended
                list2: LIST after object is appended
                list3: LIST after object is appended
    """
    list1.append(object1)
    list2.append(object2)
    list3.append(object3)
    return list1, list2, list3


def get_path_from_list(list1_object, list2_object):
    """
    Function receives 2 list objects and returns two file paths
    :param list1_object: Indexed STR Object from LIST
    :param list2_object: Indexed STR Object from LIST
    :return:    path1: STR of file path
                path2: STR of file path
    """
    try:
        path1 = list1_object
        path2 = list2_object
    except IndexError:
        logger.error('IndexError: Check the number of files in the input folders')
    return path1, path2
