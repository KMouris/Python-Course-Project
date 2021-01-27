class RasterCalculations:
    def __init__(self, snow_start_of_month, snow_cover, snow_measured):
        self.snow_start_of_month = snow_start_of_month
        self.snow_cover = snow_cover
        self.snow_measured = snow_measured

    def snow_at_end(self): # remark Kilian; maybe better to use sth with start of month instead of measured
        """

        :return:
        """
        snow_end_of_month = self.snow_start_of_month * self.snow_cover
        return snow_end_of_month

    def snowmelt(self, snow_end_of_month):
        """
        Substracts actual snow height from calculated snowsum to get snowmelt
        :param snow_end_of_month: actual snow height per month
        :return: height of snow that acts as snowmelt per month
        """
        snowmelt = self.snow_start_of_month - snow_end_of_month
        return snowmelt

    def snow_at_start(self, snow_end_of_month):
        """

        :param snow_end_of_month:
        :return:
        """
        snow_start_of_month = self.snow_measured + snow_end_of_month
        return snow_start_of_month


