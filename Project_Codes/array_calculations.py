from log import *


class ArrayCalculations:
    """
    Class author: Theresa
    CLass for mathematical operations on arrays to calculate snow depths.

    Attributes:
        snow_start_of_period: ARRAY of snow depth at start of period
        snow_cover: ARRAY of satellite data of snow cover
        snow_measured: ARRAY of measured snow depth

    Methods:
        snow_at_end(): Multiply snow at start of period with satellite data of snow cover.
        snowmelt(snow_end_of_period): Subtract actual snow depth from calculated snowsum.
        snow_at_start(snow_end_of_period): Add actual snow depth transferred from previous month and measured snow
                                           depth.
    """

    def __init__(self, snow_start_of_period, snow_cover, snow_measured):
        """
        Assign values to class attributes when a new instance is initiated.
        :param snow_start_of_period: ARRAY of snow depth at start of period
        :param snow_cover: ARRAY of satellite data of snow cover
        :param snow_measured: ARRAY of measured snow depth
        """
        self.snow_start_of_period = snow_start_of_period
        self.snow_cover = snow_cover
        self.snow_measured = snow_measured

    def snow_at_end(self):
        """
        Multiply snow at start of period with satellite data of snow cover.
        :return: ARRAY of actual snow depth at end of period
        """
        try:
            snow_end_of_period = self.snow_start_of_period * self.snow_cover
            return snow_end_of_period
        except TypeError:
            logger.error("TypeError: Arguments have to be arrays of the same type.")

    def snowmelt(self, snow_end_of_period):
        """
        Subtract actual snow depth from calculated snowsum.
        :param snow_end_of_period: ARRAY of actual snow depth at end of period
        :return: ARRAY of depth of snow that acts as snowmelt
        """
        try:
            snowmelt = self.snow_start_of_period - snow_end_of_period
            return snowmelt
        except TypeError:
            logger.error("TypeError: Arguments have to be arrays of the same type.")

    def snow_at_start(self, snow_end_of_period):
        """
        Add actual snow depth transferred from previous month and measured snow depth.
        :param snow_end_of_period: ARRAY of actual snow depth at end of period
        :return: ARRAY of snow depth at start of period
        """
        try:
            snow_start_of_period = self.snow_measured + snow_end_of_period
            return snow_start_of_period
        except TypeError:
            logger.error("TypeError: Arguments have to be arrays of the same type.")
