class RasterCalculations:
    def __init__(self, snow_start_of_month, snow_cover, snow_measured):
        self.snow_start_of_month = []
        self.snow_cover = []
        self.snow_measured = []

    def snow_at_end(self, snow_start_of_month, snow_cover): # remark Kilian; maybe better to use sth with start of month instead of measured
        """
        
        :param snow_start_of_month:
        :param snow_cover: satellite data of snow situation per month
        :return: 
        """
        try:
            snow_end_of_month = snow_start_of_month * snow_cover
        except ValueError:
            print("Arrays of the same shape have to be used.")
        except TypeError:
            print("Arrays of the same type have to be used.")
        return snow_end_of_month

    def snowmelt(self, snow_end_of_month, snow_start_of_month):
        """
        Substracts actual snow height from calculated snowsum to get snowmelt
        :param snow_end_of_month: actual snow height per month
        :param snow_start_of_month: sum of measured snow height and snow height transferred from previous month
        :return: height of snow that acts as snowmelt per month
        """
        snowmelt = snow_start_of_month - snow_end_of_month
        return snowmelt

    def snow_at_start(self, snow_measured, snow_end_of_month):
        """

        :param snow_measured: measured snow height per month
        :param snow_end_of_month:
        :return:
        """
        snow_start_of_month = snow_measured + snow_end_of_month
        return snow_start_of_month


