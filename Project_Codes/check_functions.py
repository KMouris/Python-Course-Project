from config import *


class CheckInputData:
    def __init__(self, array_one, array_two, raster_one_path, raster_two_path, datatype='float32'):
        self.array_one = array_one
        self.array_two = array_two
        self.raster_one_path = raster_one_path
        self.raster_two_path = raster_two_path
        self.datatype = datatype

    def compare_shape(self):
        """
        Compare number of rows and columns of two arrays
        """
        if not self.array_one.shape == self.array_two.shape:
            if not self.array_one.shape[0] == self.array_two.shape[0]:
                print("Unequal number of rows.")
            else:
                print("Unequal number of columns.")
        # else:
        # print("Arrays have the same shape.")

    def number_of_items(self, object_one, object_two):
        """
        Compare number of items of two objects
        """
        if not len(object_one) == len(object_two):
            if len(object_one) < len(object_two):
                print("More items in object_two.")
            else:
                print("More items in object_one.")
        else:
            print("Same number of items.")

    def compare_geotransform(self):
        """
        Round geotransformation of two Raster off to four decimal places and compare them
        """
        raster_one_gt = gdal.Open(self.raster_one_path).GetGeoTransform()
        raster_two_gt = gdal.Open(self.raster_two_path).GetGeoTransform()
        for i in range(0, 6, 1):
            if not round(raster_one_gt[i], 4) == round(raster_two_gt[i], 4):
                print("Geotransformation data at index " + str(i) + " differs from each other. ")
                # if i == 0:
                # print("Upper Left Corner is different.") usw.

    def compare_projection(self):
        """
        Compare projection of two Raster
        """
        raster_one_proj = gdal.Open(self.raster_one_path).GetProjection()
        raster_two_proj = gdal.Open(self.raster_two_path).GetProjection()
        if not raster_one_proj == raster_two_proj:
            print("Raster have different Projections.")
