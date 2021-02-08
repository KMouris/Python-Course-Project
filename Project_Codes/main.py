from check_functions import *
from statistics import *
from fun import *

start_time = time.time()

# User Input
# Folder with snow values
Snow_mm_path = r'' + os.path.abspath('../Input_Data/Snow_per_month/')
# Folder with satellite data
SnowCover_path = r'' + os.path.abspath('../Input_Data/SnowCover/')
# Folder for the results
path_results = r'' + os.path.abspath('../Results')


@wrap(entering, exiting)
def main():
    # Get all file paths into a list: All rasters must be .tif files. if not, the type of file must also be changed.
    snow_mm_paths = sorted(glob.glob(Snow_mm_path + "\\*.tif"))
    snow_cover_paths = sorted(glob.glob(SnowCover_path + "\\*.tif"))
    # Create folder if it does not already exist
    data_manager = DataManagement(path=path_results, filename=snow_mm_paths[0])
    data_manager.folder_creation()

    # loop trough input rasters, write raster arrays and corresponding dates in nested lists
    date, snow_mm, snow_cover = raster2nested_list(snow_mm_paths, snow_cover_paths)

    # get projection and geotransformation of input raster
    gt, proj = data_manager.get_proj_data()

    # Check Data
    j = 0
    for file in snow_mm:
        check_data = CheckInputData(array_one=snow_mm[j], array_two=snow_cover[j],
                                    raster_one_path=snow_mm_paths[j], raster_two_path=snow_cover_paths[j],
                                    datatype='float64')
        check_data.compare_shape()
        check_data.compare_projection()
        check_data.compare_geotransform()
        j += 1

    check_data.number_of_items(snow_mm, snow_cover)

    # Calculations
    snow_end_month, snowmelt = calculate_snowmelt(snow_mm[0], snow_mm, snow_cover)

    # Saving arrays as raster
    k = 0
    for entry in snowmelt:
        save_path = r'' + os.path.abspath('../Results/Snow_end_month') + "/snow_end_month" + str(
            date[k][0]) + ".tif"
        DataManagement.save_raster(save_path, snow_end_month[k], gt, proj)
        save_path = r'' + os.path.abspath('../Results/Snowmelt') + "/snowmelt" + str(
            date[k][0]).strip() + ".tif"
        DataManagement.save_raster(save_path, snowmelt[k], gt, proj)
        k += 1

    # Calculate Statistics (first idea, we could also write a table with statistic summary)
    raster_file = r'' + os.path.abspath('../Results/Snow_end_month/snow_end_month18_1.tif')
    shape_zone = r'' + os.path.abspath('../Input_Data/Shape_files/catchment_kokel.shp')
    get_zon_statistics(raster_file, shape_zone)

    print('Total time: ', time.time() - start_time, 'seconds')


if __name__ == '__main__':
    main()
