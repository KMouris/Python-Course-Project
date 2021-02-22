from config import *


class ZonStatistics:
    def __init__(self, path_raster, shape, datelist):
        """

        :param path_raster:
        :param shape:
        :param datelist:
        """
        self.path_raster = path_raster
        self.shape = shape
        self.datelist = datelist

    def get_zon_statistic(self):
        """
        Method which creates a dataframe containing necessary information to plot the results
        User defines the statistical value which should be plotted (here: Coverage)
        :return: df_statistics: pd.DataFrame which contains date and statistical values
        """
        # instantiate list to store the statistic values
        list_statistics = []
        i = 0
        for entry in self.path_raster:
            # get the statistical values for each raster file
            statistical_values = self.calc_zon_statistics(i)
            # get the desired statistic value to plot (here: coverage)
            value_to_plot = ([d['coverage'] for d in statistical_values])
            # append values to the list
            list_statistics.append(value_to_plot)
            i += 1
        # create and merge dataframes
        df_statistics = pd.DataFrame(list_statistics, columns=['Snow Coverage'])
        df_date = pd.DataFrame(self.datelist, columns=['Date'])
        df_statistics = df_statistics.join(df_date)
        return df_statistics

    def calc_zon_statistics(self, list_entry):
        """
        Method which calculates several statistical values
        :param list_entry: INT which identifies the raster to calculate the statistical values
        :return: stats: LIST which contains the statistical values per raster
        """
        file = self.path_raster[list_entry]
        zone = self.shape
        # calculate zonal statistics
        stats = rs.zonal_stats(zone, file, stats=['min', 'mean', 'max', 'range', 'sum'],
                               add_stats={'coverage': self.coverage})
        return stats

    def plot_zon_statistics(self):
        """
        Method which plots the desired statistical value over time and writes a .png-image
        :return:
        """
        ax = plt.gca()
        self.get_zon_statistic().plot(y="Snow Coverage", x="Date", kind='line', marker='o', color='grey',
                                         grid='major', ax=ax)
        ax.set_xlabel("Date [YY_mm]")
        ax.set_ylabel("Snow Coverage [%]")
        plt_name = 'statistic_plot'
        plt.savefig(plot_result + r'//' + plt_name, dpi=300, bbox_inches='tight')
        plt.show()

    @staticmethod
    def coverage(raster_array):
        """
        Custom statistic to calculate the percentage of values above zero (e.g. snow coverage, or areas of snow melt)
        :param raster_array: NUMPY.MASKEDARRAY containing the values of a raster (raster array)
        :return: INT which equals the percentage of values above zero
        """
        rows = len(raster_array)
        columns = len(raster_array[0])
        total_len = rows * columns
        nan_count = np.count_nonzero(np.isnan(raster_array))
        return ((np.count_nonzero(raster_array) - nan_count) / (total_len - nan_count)) * 100