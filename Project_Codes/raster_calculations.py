from config import *
from log import *


class RasterCalculations:
    def __init__(self, snow_start_of_period, snow_cover, snow_measured):
        """
        :param snow_start_of_period: ARRAY of snow depth at start of period
        :param snow_cover: ARRAY of satellite data of snow cover
        :param snow_measured: ARRAY of measured snow depth
        """
        self.snow_start_of_period = snow_start_of_period
        self.snow_cover = snow_cover
        self.snow_measured = snow_measured

    def __add__(self, other):
        try:
            np.add(self, other)
        except TypeError:
            logger.error("TypeError: Arguments have to be arrays of the same type.")
            print("Arguments have to be arrays of the same type.")

    def __mul__(self, other):
        try:
            np.multiply(self, other)
        except TypeError:
            # logger.error("TypeError: Arguments have to be arrays of the same type.")
            print("Arguments have to be arrays of the same type.")

    def __sub__(self, other):
        try:
            np.subtract(self, other)
        except TypeError:
            logger.error("TypeError: Arguments have to be arrays of the same type.")
            # print("Arguments have to be arrays of the same type.")

    def snow_at_end(self):
        """
        Multiply snow at start of period with satellite data of snow cover
        :return: ARRAY of actual snow depth at end of period
        """
        snow_end_of_period = self.snow_start_of_period * self.snow_cover
        return snow_end_of_period

    def snowmelt(self, snow_end_of_period):
        """
        Subtract actual snow depth from calculated snowsum
        :param snow_end_of_period: ARRAY of actual snow depth at end of period
        :return: ARRAY of depth of snow that acts as snowmelt
        """
        snowmelt = self.snow_start_of_period - snow_end_of_period
        return snowmelt

    def snow_at_start(self, snow_end_of_period):
        """
        Add actual snow depth transferred from previous month and measured snow depth
        :param snow_end_of_period: ARRAY of actual snow depth at end of period
        :return: ARRAY of snow depth at start of period
        """
        snow_start_of_period = self.snow_measured + snow_end_of_period
        return snow_start_of_period
