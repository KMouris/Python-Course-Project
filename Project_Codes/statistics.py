from config import *
from fun import *


def get_statistic_df(path, shape):  # just some ideas to prepare for plotting, more parameters can be added
    snow_result_paths = sorted(glob.glob(path_results + '\\Snow_end_month' + "\\*.tif"))
    list_statistics = []
    i = 0
    for entry in snow_result_paths:
        statistic_values = get_zon_statistics(snow_result_paths[i], shape)
        specified_value = ([d['coverage'] for d in statistic_values])
        list_statistics.append(specified_value)
        i += 1
    df_statistics = pd.DataFrame(list_statistics, columns=['Snow Coverage'])
    return df_statistics


def plot_statistics(df_to_plot):  # just a draft
    ax = plt.gca()
    ax.set_ylabel("Snow Coverage [%]")
    df_to_plot.plot(y="Snow Coverage", kind='line', marker='', color='grey', ax=ax)
    plt.show()


def get_zon_statistics(rasterpath, sh_zone):
    """

    :param rasterpath:
    :param sh_zone:
    :return:
    """
    file = rasterpath
    zone = sh_zone

    # calculate zonal statistics
    stats = rs.zonal_stats(zone, file, stats=['min', 'mean', 'max', 'range', 'sum'],
                           add_stats={'coverage': coverage})
    return stats


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
