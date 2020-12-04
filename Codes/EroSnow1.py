import glob
import os, sys
import pandas as pd
import numpy as np
import gdal
import osr

sys.path.append(
    r'C:/Users/Mouris/git/dirtx/geo-utils/geo-utils/')  # Of course: replace "D:/Target/Directory/", e.g., with  r'' + os.path.abspath('')
import geo_utils as gu

# Folder Directories
path = r'P:\aktiv\2018_DLR_DIRT-X\300 Modelling\310 Models\01_Erosion_model\08_Snow\Test_Spring_2018\Tests\CSVperCell'

driver_list = [str(gdal.GetDriver(i).GetDescription()) for i in range(gdal.GetDriverCount())]
driver_list.sort()
print(", ".join(driver_list[:]))

# Input values
T_snow = 0

# Original Raster Information
original_rows = 115
original_columns = 170
xllcorner = 350000.000000
yllcorner = 4445000.000000
cellsize = 1000
nodata = -9999.0


# Snow or Rain Distinguishment
def Snow_ident(Station):
    df_snow = pd.DataFrame([])
    iterations = Station.shape[0]  # Indicates the number of rows, which equals the number of iterations
    for i in range(0, iterations):  # For each row (For each date)
        df_snow.at[i, 'Total Precipitation (mm)'] = Station[i, 6]
        if Station[i, 7] < T_snow:
            df_snow.at[i, 'Snow (mm)'] = Station[i, 6]
            df_snow.at[i, 'Rain (mm)'] = 0
        else:
            df_snow.at[i, 'Rain (mm)'] = Station[i, 6];
            df_snow.at[i, 'Snow (mm)'] = 0
    return df_snow


# Calculate snow and rain per period and station
def snow_station(station, snow):
    snow_station = pd.DataFrame([])
    y = station[1, 8]
    x = station[1, 9]
    cellx = x
    celly = y
    snow_station.at[1, 'Cellx'] = cellx
    snow_station.at[1, 'Celly'] = celly
    snow_station.at[1, 'Total Prec (mm)'] = snow['Total Precipitation (mm)'].sum(axis=0)
    snow_station.at[1, 'Rain (mm)'] = snow['Rain (mm)'].sum(axis=0)
    snow_station.at[1, 'Snow (mm)'] = snow['Snow (mm)'].sum(axis=0)

    return snow_station


# Main Code
filenames = glob.glob(
    path + "\*.csv")  # Get all the .csv files in the input folder, and save the names in a list, to iterate thru them
i = 0  # to iterate in file names

# create lists for cellname, Prec, Rain and Snow
Cellx = []
Celly = []
Prec = []
Rain = []
Snow = []

for file in filenames:
    station_file = np.array(pd.read_csv(file,
                                        delimiter=','))  # Save data from each .csv file into a Numpy Array [assumes input file has a header row, which must be ignored)
    name = os.path.basename(filenames[i])  # Get name of the file, including file extension
    print("File: ", name)

    # Calculate snow and rain precipitation per hour
    snow = Snow_ident(station_file)

    # Calculate snow and rain per period and station
    SnowperStation = snow_station(station_file, snow)

    # append cell specific values to list (much faster than df.append)
    Cellx.append(SnowperStation['Cellx'].values)
    Celly.append(SnowperStation['Celly'].values)
    Prec.append(SnowperStation['Total Prec (mm)'].values)
    Rain.append(SnowperStation['Rain (mm)'].values)
    Snow.append(SnowperStation['Snow (mm)'].values)

    i += 1  # Add to counter

# Create df containing all information from lists
cell_result = pd.DataFrame(
    {'Cellx': Cellx, 'Celly': Celly, 'Total Precipitation (mm)': Prec, 'Rain (mm)': Rain, 'Snow (mm)': Snow})
np.savetxt('CellResult', cell_result, fmt='%s')

# preparing result array snow
result_array_snow = np.full(((original_rows, original_columns)), nodata)
for m in range(0, original_rows):
    for k in range(0, original_columns):
        if m in cell_result['Celly'].values and k in cell_result['Cellx'].values:
            value = cell_result['Snow (mm)'].loc[(cell_result['Celly'] == m) & (cell_result['Cellx'] == k)]
        else:
            value = nodata
        try:
            result_array_snow[m, k] = value  # save value to the corresponding row-column
        except ValueError:
            result_array_snow[m, k] = nodata

# preparing result array rain
result_array_rain = np.full(((original_rows, original_columns)), nodata)
for m in range(0, original_rows):
    for k in range(0, original_columns):
        if m in cell_result['Celly'].values and k in cell_result['Cellx'].values:
            value = cell_result['Rain (mm)'].loc[(cell_result['Celly'] == m) & (cell_result['Cellx'] == k)]
        else:
            value = nodata
        try:
            result_array_rain[m, k] = value  # save value to the corresponding row-column
        except ValueError:
            result_array_rain[m, k] = nodata

# creating raster files
res_snow = result_array_snow # origin is always top left!
# create raster files 1 km grid
gu.create_raster(
    r"P:\aktiv\2018_DLR_DIRT-X\300 Modelling\310 Models\01_Erosion_model\08_Snow\Test_Spring_2018\Tests\Raster\Snow_test.tif",
    res_snow, pixel_width=1000, pixel_height=1000, origin=(350000, 4560000), nan_val=-9999, rdtype=gdal.GDT_Float32,
    geo_info=False, epsg = 32634)

res_rain = result_array_rain
gu.create_raster(
    r"P:\aktiv\2018_DLR_DIRT-X\300 Modelling\310 Models\01_Erosion_model\08_Snow\Test_Spring_2018\Tests\Raster\Rain_test.tif",
    res_rain, pixel_width=1000, pixel_height=1000, origin=(350000, 4560000), nan_val=-9999, rdtype=gdal.GDT_Float32,
    geo_info=False, epsg = 32634)


# convert 1 km grid to 25 m grid (no IDW, so no final solution)
options = gdal.WarpOptions(resampleAlg='near', xRes=25, yRes=25)
gdal.Warp('P:\\aktiv\\2018_DLR_DIRT-X\\300 Modelling\\310 Models\\01_Erosion_model\\08_Snow\\Test_Spring_2018\\Tests\\Raster\\Rain_test_r.tif','P:\\aktiv\\2018_DLR_DIRT-X\\300 Modelling\\310 Models\\01_Erosion_model\\08_Snow\\Test_Spring_2018\\Tests\\Raster\\Rain_test.tif', options=options)
gdal.Warp('P:\\aktiv\\2018_DLR_DIRT-X\\300 Modelling\\310 Models\\01_Erosion_model\\08_Snow\\Test_Spring_2018\\Tests\\Raster\\Snow_test_r.tif', 'P:\\aktiv\\2018_DLR_DIRT-X\\300 Modelling\\310 Models\\01_Erosion_model\\08_Snow\\Test_Spring_2018\\Tests\\Raster\\Snow_test.tif', options=options)

# Maybe clipping and snapping afterwards is needed