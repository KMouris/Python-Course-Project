from config import *
from log import *


class CompareData:
    """
    Class author: Theresa
    Class for comparing different properties of arrays, objects and rasters.

    Attributes:
        array_one: ARRAY to be compared
        array_two: ARRAY to be compared
        raster_one_path: STRING of raster path to be compared
        raster_two_path: STRING of raster path to be compared

    Methods:
        compare_shape(): Compare number of rows and columns of two arrays.
        number_of_items(object_one, object_two): Compare number of items of two objects.
        compare_geotransform(): Round the geotransformation values off to four decimal places and compare them.
        compare_projection(): Compare the projection of two rasters.
    """

    def __init__(self, array_one, array_two, raster_one_path, raster_two_path):
        """
        Assign values to class attributes when a new instance is initiated.
        :param array_one: ARRAY to be compared
        :param array_two: ARRAY to be compared
        :param raster_one_path: STRING of raster path to be compared
        :param raster_two_path: STRING of raster path to be compared
        """
        self.array_one = array_one
        self.array_two = array_two
        self.raster_one_path = raster_one_path
        self.raster_two_path = raster_two_path

    def compare_shape(self):
        """Compare number of rows and columns of two arrays."""
        try:
            if not self.array_one.shape == self.array_two.shape:
                if not self.array_one.shape[0] == self.array_two.shape[0]:
                    logger.warning("Unequal number of rows.")
                else:
                    logger.warning("Unequal number of columns.")
        except AttributeError:
            logger.error("Attribute Error: Input arguments have to be arrays.")

    @staticmethod
    def number_of_items(object_one, object_two):
        """
        Compare the number of items of two objects.
        :param object_one: Object on which the len() function can be applied
        :param object_two: Object on which the len() function can be applied
        :return:
        """
        try:
            if not len(object_one) == len(object_two):
                if len(object_one) < len(object_two):
                    logger.warning("More items in object_two.")
                else:
                    logger.warning("More items in object_one.")
        except TypeError:
            logger.error("TypeError: Type of provided object has no len().")

    def compare_geotransform(self):
        """Round geotransformation of two rasters off to four decimal places and compare them."""
        try:
            raster_one_gt = gdal.Open(self.raster_one_path).GetGeoTransform()
        except FileNotFoundError:
            logger.error("FileNotFoundError: The raster path %s does not exist." % self.raster_one_path)
        try:
            raster_two_gt = gdal.Open(self.raster_two_path).GetGeoTransform()
        except FileNotFoundError:
            logger.error("FileNotFoundError: The raster path %s does not exist." % self.raster_two_path)
        for i in range(0, 6, 1):
            if not round(raster_one_gt[i], 4) == round(raster_two_gt[i], 4):
                logger.warning("Geotransformation data at index " + str(i) + " differs from each other. ")

    def compare_projection(self):
        """Compare the projection of two rasters."""
        try:
            raster_one_proj = gdal.Open(self.raster_one_path).GetProjection()
        except FileNotFoundError:
            logger.error("FileNotFoundError: The raster path %s does not exist." % self.raster_one_path)
        try:
            raster_two_proj = gdal.Open(self.raster_two_path).GetProjection()
        except FileNotFoundError:
            logger.error("FileNotFoundError: The raster path %s does not exist." % self.raster_two_path)
        if not raster_one_proj == raster_two_proj:
            logger.error("Raster have different Projections.")
