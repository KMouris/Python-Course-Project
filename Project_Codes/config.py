"""config.py contains the required user input (e.g. input and output folder paths, settings for the statistical
calculation) and the handling of packages """
# import all needed basic python libraries
try:
    import glob
    import logging
    import os
    import sys
    import time
except ModuleNotFoundError as b:
    print('ModuleNotFoundError: Missing basic libraries (required: glob, logging, os, sys, time')
    print(b)

# import additional python libraries
try:
    import gdal
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    import rasterstats as rs
    import scipy
except ModuleNotFoundError as e:
    print('ModuleNotFoundError: Missing fundamental packages (required: gdal, maptlotlib.pyplot, numpy, '
          'pandas, rasterstats, scipy')
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
snow_path_mm = r'' + os.path.abspath('../Input_Data/Snow_per_month/')
# Folder with satellite data
snow_cover_path = r'' + os.path.abspath('../Input_Data/SnowCover/')
# Folder for the results
path_results = r'' + os.path.abspath('../Results')

# Input for statistics
# Folder with calculated results to be used for statistical calculations
snow_result_paths = sorted(glob.glob(path_results + '\\Snow_end_month' + "\\*.tif"))
# Location of shapefile used for zonal statistics
shape_zone = r'' + os.path.abspath('../Input_Data/Shape_files/catchment_kokel.shp')
# Definition of statistical parameter to be plotted ('min', 'mean', 'max', 'range', 'sum', 'coverage')
statistical_param = 'coverage'
# Disable (False) or enable (True) plot
plot_statistic = True

# Output folder for plots
plot_result = path_results + '\\Plots'
