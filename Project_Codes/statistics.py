from config import *


def get_zon_statistics(rasterpath, shape_zone):
    """

    :param rasterpath:
    :param shape_zone:
    :return:
    """
    file = rasterpath
    zone = shape_zone

    # calculate zonal statistics
    stats = rs.zonal_stats(zone, file, stats=['min', 'mean', 'max', 'range', 'sum'],
                           add_stats={'coverage': coverage})
    print(stats)

    # maybe add function which calculates snow covered areas


# custom statistic which calculates the (snow) coverage in %
def coverage(raster_array):
    """
    Custom statistic to calculate the the percentage values above zero (e.g. snow coverage, or areas of snow melt)
    :param raster_array:
    :return:
    """
    rows = len(raster_array)
    columns = len(raster_array[0])
    total_len = rows * columns
    nan_count = np.count_nonzero(np.isnan(raster_array))
    return ((np.count_nonzero(raster_array) - nan_count) / (total_len - nan_count)) * 100
