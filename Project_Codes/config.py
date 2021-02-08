try:
    import gdal
    import glob
    import logging
    import numpy as np
    import os
    import rasterstats as rs
    import scipy
    import sys
    import time

except ModuleNotFoundError as e:
    print('ModuleNotFoundError: Missing fundamental packages (required: gdal, glob, numpy, os, scipy, sys, time).')
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

