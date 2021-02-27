from config import *
from log import *


class DataManagement:
    """
    Class author: Kilian
    Class with useful and robust methods for managing output folders, extracting information from raster files and
    writing raster files using the previously extracted information.

    Attributes:
        path: STR of path needed to manage output folders
        filename: STR of filename

    Methods:
        folder_creation(): Method creates folder at instantiated path if it does not already exists.
        get_date(): Method gets the month and the year from the instantiated filenames.
        create_date_string(): Method which returns a date string by calling the get_date method.
        get_proj_data(): Method which get the projection and geotransformation from a raster file (osgeo.gdal.Dataset).
        save_raster(res_path, array, gt, proj): Static Method which creates and saves raster-file (.tif) from an
                                                existing array using a defined projection.

    """
    def __init__(self, path, filename):
        """
        Assign values to class attributes when a new instance is initiated.
        :param path: STR of path needed to manage output folders
        :param filename: STR of filename
        """
        self.path = path
        self.filename = filename

    def folder_creation(self):
        """
        Method creates folder at instantiated path if it does not already exists
        :return: None
        """
        try:
            # check if folder exists, if not create folder
            if not os.path.exists(self.path):
                logger.info("Creating folder: %s " % self.path)
                os.makedirs(self.path)
            if not os.path.exists(self.path + "\\Snowmelt"):
                logger.info("Creating folder: %s " % self.path + "\\Snowmelt")
                os.makedirs(self.path + "\\Snowmelt")
            if not os.path.exists(self.path + "\\Snow_end_month"):
                logger.info("Creating folder: %s " % self.path + "\\Snow_end_month")
                os.makedirs(self.path + "\\Snow_end_month")
            if not os.path.exists(self.path + "\\Plots"):
                logger.info("Creating folder: %s " % self.path + "\\Plots")
                os.makedirs(self.path + "\\Plots")
            else:
                logger.info("The folder already exists and is not created")
            return 0
        except OSError as o:
            logger.error("OSError: Directory could not be created")
            print(o)
            pass

    def get_date(self):
        """
        Method gets the month and the year from the instantiated filenames
        :return:    sm_month:  INT specifying the month
                    sm_year:   INT specifying the year
        """
        try:
            sm_year = int((self.filename[-9]) + (self.filename[-8]))
            sm_month = int((self.filename[-6]) + (self.filename[-5]))
            return sm_month, sm_year
        except ValueError as v:
            logger.error("ValueError: Invalid file name. Please make sure that the file name consists of 14 characters "
                         "and contains month and year (YY_mm)")
            print(v)

    def create_date_string(self):
        """
        Method which returns a date string by calling the get_date method
        :return: datestring: STR in the format (YY_mm)
        """
        # get month and year from get_date() method
        sm_month, sm_year = self.get_date()
        # create date string (Format: YY/mm)
        datestring = (str(sm_year) + '_' + str(sm_month))
        return datestring

    def get_proj_data(self):
        """
        Method which get the projection and geotransformation from a raster file (osgeo.gdal.Dataset)
        :return: gt: TUPLE defining a gdal.DataSet.GetGeoTransform object
                 proj: STR defining a gdal.DataSet.GetProjection object
        """
        try:
            raster = gdal.Open(self.filename)  # Extract raster from path
        except RuntimeError as re:
            logger.error("RuntimeError: Raster can't be accessed")
            print(re)
            sys.exit(1)  # code shouldn't run any further if this error occurs
        gt = raster.GetGeoTransform()  # Get geotransformation data
        proj = raster.GetProjection()  # Get projection of raster
        return gt, proj  # Return both variables

    @staticmethod
    def save_raster(res_path, array, gt, proj):
        """
        Static Method which creates and saves raster-file (.tif) from an existing array using a defined projection
        and geotransformation data
        :param res_path: STR of path and result filename
        :param array: NUMPY.NDARRAY of values to rasterize
        :param gt: TUPLE defining a gdal.DataSet.GetGeoTransform object
        :param proj: STR defining a gdal.DataSet.GetProjection object
        :return: saves raster file in the selected dir (path) : osgeo.gdal.Dataset (uses GTiff driver)
        """
        # Get drivers to save outputs as raster .tif files
        driver = gdal.GetDriverByName("GTiff")
        driver.Register()

        # Instantiate the raster files to save, providing all needed information
        outrs = driver.Create(res_path, xsize=array.shape[1], ysize=array.shape[0], bands=1, eType=gdal.GDT_Float32)

        # Assign raster data and assign the array to the raster
        outrs.SetGeoTransform(gt)  # Set geo transform data
        outrs.SetProjection(proj)  # Set projection
        outband = outrs.GetRasterBand(1)  # Create a band in which the array will be written
        outband.WriteArray(array)  # Write array into band
        outband.SetNoDataValue(np.nan)  # Set no data value as np.nan
        outband.ComputeStatistics(0)  # Compute and include standard raster statistics

        # Release raster band
        outband.FlushCache()

        logger.info("Saved raster: %s " % os.path.basename(res_path))
        return 0
