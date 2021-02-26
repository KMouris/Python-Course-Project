# Effect of snow on soil erosion - snowpack dynamics

# Introduction
The overall goal of the project is to extend the Revised Universal Soil Loss Equation RUSLE ([Renard, 1997](https://www.ars.usda.gov/arsuserfiles/64080530/rusle/ah_703.pdf))
by including the effects of snowfall and snowmelt on soil erosion. 
The first step is to distinguish between precipitation in the form of rain (erosive) or snow (non-erosive). 
Additionally, snow-covered areas are detected at the end of each month using freely available satellite data (e.g. Sentinel-2). 
These two steps precede the presented code and have already been automated. 
>  
The aim of the presented code is to calculate monthly snowpack dynamics and to identify monthly snowmelt to later incorporate its erosive forces.
The results are written as georeferenced raster files (.tif format) and can be accessed by all common GIS programs. 
Optionally, the user can plot various statistical values (e.g. snow cover) over time. 
If only a subarea is of interest, this can be defined by a shapefile. The previously calculated snowfall (mm) and the identified snow cover serve as input data. 
The following figure provides a highly simplified overview. Details can be found in the code diagram and the code description.

# Requirements
*Python* libraries: *geo_utils*, *gdal*, *matplotlib.pyplot*, *numpy*, *pandas*, *rasterstats*, *scipy*
>  
*Standard* libraries: *glob*, *logging*, *os*, *sys*, *time*

# Code diagram

# Code description

## config.py
File where all required libraries and global variables are loaded. 
````python
try:
    import gdal
    import glob
    import logging
    import matplotlib.pyplot as plt
    import numpy as np
    import os
    import pandas as pd
    import rasterstats as rs
    import scipy
    import sys
    import time

except ModuleNotFoundError as e:
    print('ModuleNotFoundError: Missing fundamental packages (required: gdal, glob, numpy, os, pandas, scipy, sys, '
          'time).')
    print(e)

try:
    sys.path.append(
        r'' + os.path.abspath(
            '../geo-utils/'))
    import geo_utils as gu
except ModuleNotFoundError:
    print("ModuleNotFoundError: Cannot import geo_utils")

# User Input
# Folder with snow values
Snow_mm_path = r'' + os.path.abspath('../Input_Data/Snow_per_month/')
# Folder with satellite data
SnowCover_path = r'' + os.path.abspath('../Input_Data/SnowCover/')
# Folder for the results
path_results = r'' + os.path.abspath('../Results')

# Input for statistics
snow_result_paths = sorted(glob.glob(path_results + '\\Snow_end_month' + "\\*.tif"))
shape_zone = r'' + os.path.abspath('../Input_Data/Shape_files/catchment_kokel.shp')
````

## log.py
File where logger is set up. 

## data_management.py
File where `DataManagement` class is stored which provides following methods:

### `__init__()`
Class with useful and robust methods for managing output folders, extracting information from raster files and writing raster files using the previously extracted information.
Assigns values to class attributes when a new instance is initiated. 

| Input argument | Type | Description |
|-----------------|------|-------------|
|`path`| STRING | Path needed to manage output folders |
|`filename`| STRING | Filename |

### `folder_creation()`

Method creates folder at instantiated path, if it does not already exists.

**return:** None

###  `get_date()`

Method gets the month and the year from the instantiated filenames.

**return:** INTEGERs `sm_year`,`sm_month`

### `create_date_string()`

Method which returns a date string by calling the get_date method.

**return:** STRING `datestring`

### `get_proj_data()`

Method which get the projection and geotransformation from a raster file (osgeo.gdal.Dataset)

**return:** TUPLE `gt`, STRING `proj`

### `save_raster()`

Static Method which creates and saves raster-file (.tif) from an existing array using a defined projection and geotransformation data.

| Input argument | Type | Description |
|-----------------|------|-------------|
|`res_path`| STRING | Path and result filename |
|`array`| ARRAY | Values to rasterize |
|`gt`| TUPLE | gdal.DataSet.GetGeoTransform object |
|`proj`| STRING | gdal.DataSet.GetProjection object |

**return:** None

## raster_calculations.py
File where `RasterCalculations` class is stored which provides following methods:

### `__init__()`

Assigns values to class attributes when a new instance is initiated. 

| Input argument | Type | Description |
|-----------------|------|-------------|
|`snow_start_of_period`| ARRAY | Snow depth at start of period |
|`snow_cover`| ARRAY | Satellite data of snow cover |
|`snow_measured`| ARRAY | Measured snow depth |

### `snow_at_end()`

Calculates snow depth at the end of the period by multiplying the snow depth at the start of the period with the 
satellite data of the snow cover. 

**return:** ARRAY `snow_end_of_period`

### `snowmelt()`

Calculates snow depth acting as snowmelt by substracting the actual snow depth at the end of the period from the 
calculated snowsum at the beginning of the period.

| Input argument | Type | Description |
|----------------|------|-------------|
|`snow_end_of_period`| ARRAY | actual snow depth at end of a period |

**return:** ARRAY `snowmelt`

### `snow_at_start()`

Calculates snow depth at the beginning of a period by summing up the actual snow depth transferred from the previous 
month and the measured snow depth.

| Input argument | Type | Description |
|----------------|------|-------------|
|`snow_end_of_period`| ARRAY | actual snow depth at end of a period |

**return:** ARRAY `snow_start_of_period`

## check_functions.py
File where `CompareData` class is stored which provides following methods:

### `__init__()`

Assigns values to class attributes when new instance is initiated. 

| Input argument | Type | Description |
|----------------|------|-------------|
|`array_one`| ARRAY | arbitrary Array to be compared |
|`array_two`| ARRAY | arbitrary Array to be compared |
|`raster_one_path`| STRING | path of arbitrary raster to be compared |
|`raster_two_path`| STRING | path of arbitrary raster to be compared |

### `compare_shape()`

Compares the number of columns and the number of rows of two arrays.

### `number_of_items()`

Compares the number of items of two objects.

| Input argument | Type | Description |
|----------------|------|-------------|
|`object_one`| LIST, STRING, etc. | Object on which the `len()` function can be applied |
|`object_two`| LIST, STRING, etc. | Object on which the `len()` function can be applied |

### `compare_geotransform()`

Rounds geotransformation values of two rasters off to four decimal places and compares them.

### `compare_projection()`

Compares the projection of two rasters.

## zon_statistics.py
File where `ZonStatistics` class is stored which provides following methods:

### `__init__()`

Class with useful methods to calculate and plot zonal statistics, including a custom statistic to calculate the (snow) coverage of a zone in an raster array.
Assigns values to class attributes when new instance is initiated. 

| Input argument | Type | Description |
|-----------------|------|-------------|
|`path_raster`| LIST | Paths to raster files |
|`shape`| STRING | Path to shapefile defining the zone for calculating the statistics |
|`datelist`| LIST | Datestrings, format yy_mm |
|`parameter`| STRING | Definition of statistical parameter to be plotted |

### `get_zon_statistics()`

Method which creates a dataframe containing necessary information to plot the results.
User defines the statistical value which should be plotted in config.py (here: Coverage).

**return:** DATAFRAME `df_statistics`

### `calc_zon_statistics()`

Method which calculates several statistical values.

| Input argument | Type | Description |
|-----------------|------|-------------|
|`list_entry`| INTEGER | Identification of the raster to calculate the statistical values |

**return:** LIST `stats`

### `plot_zon_statistics()`

 Method which plots the desired statistical value over time and writes a .png-image.
 Method can be disabled in `config.py` (`plot_statistic=False`).
 
 ### `coverage()`
 
 Custom statistic to calculate the percentage of values above zero (e.g. snow coverage, or areas of snow melt).
 
| Input argument | Type | Description |
|-----------------|------|-------------|
|`raster_array`| MASKED ARRAY | Contains raster array |

**return:** INTEGER `calc_coverage`

## fun.py

The following basic functions and functions wrapping up different class methods are stored in this file:

### `snowdepth()`

Calculates the snow depth acting as snowmelt, the snow depth at the end of a period and the snow depth at the beginning
of the next period by instanciating an object of the `RasterCalculations` class.

| Input argument | Type | Description |
|----------------|------|-------------|
|`snow_at_start`| ARRAY | Snow depth at beginning of the period |
|`measured_snow_next_period`| ARRAY | Measured snow depth at the beginning of the next period |
|`satellite_data`| ARRAY | Satellite Data of the snow cover |

**return:** ARRAYs `snow_at_end_array`, `snowmelt_array`, `snow_start_array`

### `check_data()`

Compares the size of two arrays, the geotransformation and projections of two rasters and the number of items in two
objects by instanciating an object of the `CompareData` class.

| Input argument | Type | Description |
|----------------|------|-------------|
|`array_one`| ARRAY | arbitrary Array to be compared |
|`array_two`| ARRAY | arbitrary Array to be compared |
|`raster_one_path`| STRING | path of arbitrary raster to be compared |
|`raster_two_path`| STRING | path of arbitrary raster to be compared |
|`object_one`| LIST, STRING, etc. | Object on which the `len()` function can be applied |
|`object_two`| LIST, STRING, etc. | Object on which the `len()` function can be applied |

### `compare_date()`

Extracts the dates from the filenames of two rasters and compares them by instantiating an object of the
`DataManagement` class.

| Input argument | Type | Description |
|----------------|------|-------------|
|`path_raster_one`| STR | path of raster one |
|`path_raster_two`| STR | path of raster two |
|`filename_one`| STR | 

*** ***filename wird nicht benutzt*** ****

### `create_lists()`

Function which creates three empty lists. 

**return:** LISTs `list1`, `list2`, `list3`

### `append2list()`

Appends one object to one of a total of three lists.

| Input argument | Type | Description |
|----------------|------|-------------|
|`list1`| LIST | Arbitrary list |
|`list2`| LIST | Arbitrary list |
|`list3`| LIST | Arbitrary list |
|`object1`| ARRAY, INT, etc. | Object which is appendable to a list |
|`object2`| ARRAY, INT, etc. | Object which is appendable to a list |
|`object3`| ARRAY, INT, etc. | Object which is appendable to a list |

**return:** LISTs `list1`, `list2`, `list3`

### `get_path_from_list()`

Function receives 2 list objects and returns two file paths.

| Input argument | Type | Description |
|----------------|------|-------------|
|`list1_object`| STRING | Indexed string object from list|
|`list2_object`| STRING | Indexed string object from list |

**return:** STRINGs `path1`, `path2`

## main.py

