from data_management import *
from check_functions import *
from log import *


def create_lists():
    list1 = []
    list2 = []
    list3 = []
    return list1, list2, list3


def create_date_string(filenames):
    # instantiate data management object to use get_date method
    data_manager = DataManagement(path=r'' + os.path.abspath('../Results'), filename=filenames)
    sm_month, sm_year = data_manager.get_date()
    # create date string (Format: YY/mm)
    datestring = (str(sm_year) + '_' + str(sm_month))
    return datestring


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
