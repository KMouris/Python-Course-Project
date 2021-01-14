class RasterCalculations:
    def __init__(self, snow_measured, snow_cover):
        self.snow_measured
        self.snow_cover
        pass

    def snow_at_end (self, snow_measured, snow_cover):
        """
        
        :param snow_measured: 
        :param snow_cover: 
        :return: 
        """
        snow_start_of_month = snow_measured
        snow_end_of_month = snow_start_of_month * snow_cover
        return snow_end_of_month

    def snowmelt(self, snow_end_of_month, snow_measured):
        """
        Substracts actual snow height from calculated snowsum to get snowmelt
        :param snow_end_of_month: actual snow height per month
        :param snow_measured: measured snow height per month
        :return: height of snow that acts as snowmelt per month
        """
        snowmelt = snow_measured - snow_end_of_month
        return snowmelt


    def snow_at_start(self, snow_measured=[], snow_end_of_month=[]):
        """

        :param snow_measured:
        :param snow_end_of_month:
        :return:
        """
        snow_start_of_month = snow_measured + snow_end_of_month
        return snow_start_of_month


    # def actual_snow (self, snow_start_of_month, snow_measured, snow_cover):
    #  """
    #   compares precipitation data with satellite data to calculate actual snow height
    #    :param snow_measured: measured snow height per month
    #   :param snow_cover: satellite data of snow cover per month
    #    :return: actual snow at the end of the month
    #    """
    #    # raster2array + masked_array?
    #    snow_start_of_month = snow_measured
    #    snow_end_of_month = snow_start_of_month * snow_cover
    #    snow_start_of_month = snow_measured + snow_end_of_month[i-1]
    #
    #    return snow_end_of_month
    # pass




    # Design
    # for i,j in snow_mm,snow_cover:
    #   actual_snow(snow_mm, snow_cover)
    # for i in snow_mm:
    #   snowmelt(snow_end_of_month, snow_mm)