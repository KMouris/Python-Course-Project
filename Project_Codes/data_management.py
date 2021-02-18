from config import *
from log import *


class DataManagement:
    def __init__(self, path, filename):
        self.path = path
        self.filename = filename

    def folder_creation(self):
        """
        Functions creates folder to instantiated path if it does not already exists
        :return: None
        """
        try:
            if not os.path.exists(self.path):
                logger.info("Creating folder: %s " % self.path)
                os.makedirs(self.path)
            if not os.path.exists(self.path + "\\Snowmelt"):
                logger.info("Creating folder: %s " % self.path + "\\Snowmelt")
                os.makedirs(self.path + "\\Snowmelt")
            if not os.path.exists(self.path + "\\Snow_end_month"):
                logger.info("Creating folder: %s " % self.path + "\\Snow_end_month")
                os.makedirs(self.path + "\\Snow_end_month")
            else:
                logger.info("The folder already exists and is not created")
            return 0
        except OSError as o:
            logger.error('OSError: Directory could not be created')
            print(o)
            pass

    def get_date(self):
        """
        Gets the month and the year from the instantiated filenames
        :return:    sm_month:  INT specifying the month
                    sm_year:   INT specifying the month
        """
        try:
            sm_year = int((self.filename[-9]) + (self.filename[-8]))
            sm_month = int((self.filename[-6]) + (self.filename[-5]))
            return sm_month, sm_year
        except ValueError as v:
            logger.error('ValueError: Invalid file name. Please make sure that the file name consists of 14 characters '
                         'and contains the month and year.')
            print(v)
            sys.exit(1)  # code shouldn't run any further if this error occurs

    # Function receives raster file path and extracts the Geotransformation and Projection, to assign to all output
    # rasters
    def get_proj_data(self):
        """
        Function which get the Projection and Geotransformation from a raster file (osgeo.gdal.Dataset)
        :return: gt: TUPLE defining a gdal.DataSet.GetGeoTransform object
                 proj: STR defining a gdal.DataSet.GetProjection object
        """
        try:
            raster = gdal.Open(self.filename)  # Extract raster from path
        except RuntimeError as e:
            logger.error("RuntimeError: Raster can't be accessed")
            print(e)
            sys.exit(1)  # code shouldn't run any further if this error occurs
        gt = raster.GetGeoTransform()  # Get geotransformation data
        proj = raster.GetProjection()  # Get projection of raster
        return gt, proj  # Return both variables

    @staticmethod
    def save_raster(path, array, gt, proj):
        """
        Create and save raster-file (.tif) from an existing array
        :param path: STR of path and result filename
        :param array: NUMPY.NDARRAY of values to rasterize
        :param gt: TUPLE defining a gdal.DataSet.GetGeoTransform object
        :param proj: STR defining a gdal.DataSet.GetProjection object
        :return: saves raster file in the selected dir (path) : osgeo.gdal.Dataset (uses GTiff driver)
        """
        # Get drivers to save outputs as raster .tif files
        driver = gdal.GetDriverByName("GTiff")  # Get Driver
        driver.Register()  # Register driver variable

        # Create the raster files to save, providing all needed information (folder + name, number of columns (x),
        # number of rows (y), No. of bands, output data type)
        outrs = driver.Create(path, xsize=array.shape[1], ysize=array.shape[0], bands=1, eType=gdal.GDT_Float32)

        # Assign raster data and assign the array to the raster
        outrs.SetGeoTransform(gt)  # Assign geo transform data from input raster (same size)
        outrs.SetProjection(proj)  # Assign projection input raster (same projection)
        outband = outrs.GetRasterBand(1)  # Create a band in which the array will be written
        outband.WriteArray(array)  # Write array into band
        outband.SetNoDataValue(np.nan)  # Set no data value as Numpy nan
        outband.ComputeStatistics(0)  # Set the raster statistics to the output raster

        # Save raster to folder
        outband.FlushCache()

        logger.info("Saved raster: %s " % os.path.basename(path))
        return 0
