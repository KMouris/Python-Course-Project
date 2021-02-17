from statistics import *
from fun import *

start_time = time.time()


@wrap(entering, exiting)
def main():
    # Get all file paths into a list: All rasters must be .tif files. if not, the type of file must also be changed.
    snow_mm_paths = sorted(glob.glob(Snow_mm_path + "\\*.tif"))
    snow_cover_paths = sorted(glob.glob(SnowCover_path + "\\*.tif"))

    # Create folder if it does not already exist
    data_manager = DataManagement(path=path_results, filename=snow_mm_paths[0])
    data_manager.folder_creation()

    # Check dates at same index
    i = 0
    for file in snow_cover_paths:
        compare_date(Snow_mm_path, SnowCover_path, snow_mm_paths[i], snow_cover_paths[i])
        i += 1

    # loop trough input rasters, write raster arrays and corresponding dates in  lists
    date, snow_mm, snow_cover = raster2list(snow_mm_paths, snow_cover_paths)

    # get projection and geotransformation of input raster
    gt, proj = data_manager.get_proj_data()

    # Check Data
    j = 0
    for file in snow_mm:  # compares number of items in every loop
        check_input(snow_mm[j], snow_cover[j], snow_cover_paths[j], snow_cover_paths[j], snow_mm_paths, snow_cover_paths)
        j += 1

    logger.error("Calculation started.")
    # Calculations test
    snow_end_month = []
    snow_melt = []
    # initial snow has to be defined at index 0 of list
    snow_start_month = [snow_mm[0]]
    k = 0
    m = 1
    try:
        for i in snow_mm:
            snow_end_array, snowmelt_array, snow_start_array = calc_snowdepth(snow_start_month[k],
                                                                              snow_mm[m],
                                                                              snow_cover[k])
            snow_end_month.append(snow_end_array)
            snow_melt.append(snowmelt_array)
            # avoids appending wrong snow_start value of last loop to list
            if k < len(snow_mm) - 1:
                snow_start_month.append(snow_start_array)
            k += 1
            if m < len(snow_mm) - 1:
                m += 1
    except IndexError:
        print("Check number of items in list.")

    # Saving arrays as raster
    k = 0
    for entry in snow_melt:
        save_path = r'' + os.path.abspath('../Results/Snow_end_month') + "/snow_end_month" + str(
            date[k][0]) + ".tif"
        DataManagement.save_raster(save_path, snow_end_month[k], gt, proj)
        save_path = r'' + os.path.abspath('../Results/Snowmelt') + "/snowmelt" + str(
            date[k][0]) + ".tif"
        DataManagement.save_raster(save_path, snow_melt[k], gt, proj)
        k += 1

    # Calculate Statistics (first idea, we could also write a table with statistic summary)
    raster_file = r'' + os.path.abspath('../Results/Snow_end_month/snow_end_month18_3.tif')
    shape_zone = r'' + os.path.abspath('../Input_Data/Shape_files/catchment_kokel.shp')
    get_zon_statistics(raster_file, shape_zone)

    print('Total time: ', time.time() - start_time, 'seconds')


if __name__ == '__main__':
    main()
