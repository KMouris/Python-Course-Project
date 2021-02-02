class RasterCalculations:
    def __init__(self, snow_start_of_month, snow_cover, snow_measured):
        """
        :param snow_start_of_month: array of snow height at start of month
        :param snow_cover: array of satellite data
        :param snow_measured: array of measured snow height
        """
        self.snow_start_of_month = snow_start_of_month
        self.snow_cover = snow_cover
        self.snow_measured = snow_measured

    def snow_at_end(self):
        """
        compares calculated snow height with satellite data
        :return: actual snow height
        """
        try:
            snow_end_of_month = self.snow_start_of_month * self.snow_cover
            return snow_end_of_month
        except TypeError:
            print("Variables have to have same data type.")    # anstatt print könnte man logging.error benutzen

    def snowmelt(self, snow_end_of_month):
        """
        Substracts actual snow height from calculated snowsum
        :param snow_end_of_month: actual snow height
        :return: height of snow that acts as snowmelt
        """
        snowmelt = self.snow_start_of_month - snow_end_of_month
        return snowmelt

    def snow_at_start(self, snow_end_of_month):
        """
        sum of actual snow height transferred from previous month and measured snow height
        :param snow_end_of_month: actual snow height
        :return: snow height at start of month
        """
        snow_start_of_month = self.snow_measured + snow_end_of_month
        return snow_start_of_month


