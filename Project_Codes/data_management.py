import os
import gdal
import numpy as np


class DataManagement:
    def __init__(self, path, filename):
        self.path = path
        self.filename = filename

    def folder_creation(self):
        if not os.path.exists(self.path):
            print("Creating folder: ", self.path)
            os.makedirs(self.path)
        if not os.path.exists(self.path + "\\Snowmelt"):
            print("Creating folder: ", self.path + "\\Snowmelt")
            os.makedirs(self.path + "\\Snowmelt")
        if not os.path.exists(self.path + "\\Snow_start_month"):
            print("Creating folder: ", self.path + "\\Snow_start_month")
            os.makedirs(self.path + "\\Snow_start_month")
        if not os.path.exists(self.path + "\\Snow_end_month"):
            print("Creating folder: ", self.path + "\\Snow_end_month")
            os.makedirs(self.path + "\\Snow_end_month")

    # def get_date(self, filenames): # static method option
    # sm_year = int((filenames[-10]) + (filenames[-9]))
    # sm_month = int((filenames[-7]) + (filenames[-6]))
    # return sm_month, sm_year

    def get_date(self):  # option 2
        sm_year = int((self.filename[-10]) + (self.filename[-9]))
        sm_month = int((self.filename[-7]) + (self.filename[-6]))
        return sm_month, sm_year

    # Function receives raster file path and extracts the Geotransformation and Projection, to assign to all output
    # rasters
    def get_raster_data(self):
        raster = gdal.Open(self.filename)  # Extract raster from path
        gt = raster.GetGeoTransform()  # Get geotransformation data
        proj = raster.GetProjection()  # Get projection of raster
        print(proj)
        return gt, proj  # Return both variables

    # Functions receives an array to save, and the path in which to save the file. It also receies the GeoTransform and Projections of output raster
    # one Option --> maybe use Sebastian geoutils
    def save_raster(self, array, gt, proj):
        # Step 1: Get drivers in order to save outputs as raster .tif files
        driver = gdal.GetDriverByName("GTiff")  # Get Driver and save it to variable
        driver.Register()  # Register driver variable

        # #Step 2: Create the raster files to save, with all the data: folder + name, number of columns (x), number of rows (y), No. of bands, output data type (gdal type)
        outrs = driver.Create(self, xsize=array.shape[1], ysize=array.shape[0], bands=1, eType=gdal.GDT_Float32)

        # Step 3: Assign raster data and assign the array to the raster
        outrs.SetGeoTransform(gt)  # assign geo transform data from the original input raster (same size)
        outrs.SetProjection(proj)  # assign projection to raster from original input raster (same projection)
        outband = outrs.GetRasterBand(1)  # Create a band in which to input our array into
        outband.WriteArray(array)  # Read array into band
        outband.SetNoDataValue(np.nan)  # Set no data value as Numpy nan
        outband.ComputeStatistics(0)  # Set the raster statistics to the output raster

        # Step 4: Save raster to folder
        outband.FlushCache()
        outband = None
        outrs = None

        print("Saved raster: ", os.path.basename(self))

    # not used in current version, use of geoutils instead
    # Function: Receives an array, obtained from a raster, and the nodata value for the given raster and generates a masked array, in which the NODATA
    # values are "masked", so no calculations are done with such values
    def raster_to_array(self, raster_path, band_number=1):
        raster = gdal.Open(raster_path)  # Read raster file
        band = raster.GetRasterBand(band_number)  # Get raster band
        no_data = np.float32(
            band.GetNoDataValue())  # Get NoData value, since all input rasters could have different values and assign a numpy type variable
        array = np.float32(
            band.ReadAsArray())  # Save band info as array and assign the same data type as no_data to avoid inequalities
        # mask array
        masked_array = create_masked_array(array, no_data)  # Create a masked array from the input data
        return masked_array
