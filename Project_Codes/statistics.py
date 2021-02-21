from config import *
from fun import *


def get_statistic_df(path, shape, datelist):
    """
Function which creates a dataframe with the need information to plot the results
    :param path:
    :param shape:
    :param datelist:
    :return:
    """
    # instantiate list to store the statistic values
    list_statistics = []
    i = 0
    for entry in snow_result_paths:
        # get the statistical values for each raster file
        statistic_values = get_zon_statistics(path[i], shape)
        # get the desired statistic value to plot (here: coverage)
        value_to_plot = ([d['coverage'] for d in statistic_values])
        # append values to the list
        list_statistics.append(value_to_plot)
        i += 1
    # create and merge dataframes
    df_statistics = pd.DataFrame(list_statistics, columns=['Snow Coverage'])
    df_date = pd.DataFrame(datelist, columns=['Date'])
    df_statistics = df_statistics.join(df_date)
    return df_statistics


def plot_statistics(df_to_plot):
    ax = plt.gca()
    ax.set_ylabel("Snow Coverage [%]")
    df_to_plot.plot(y="Snow Coverage", x="Date", kind='line', marker='o', color='grey', ax=ax)
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
