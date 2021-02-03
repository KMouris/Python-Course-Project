try:
    import os
    import gdal
    import numpy as np
    import sys
    import glob
    import time
    import scipy
except ModuleNotFoundError as e:
    print('ModuleNotFoundError: Missing fundamental packages (required: sys, glob, time, os, gdal, numpy).')
    print(e)

try:
    sys.path.append(
        r'' + os.path.abspath(
            '../geo-utils/'))
    import geo_utils as gu
except ModuleNotFoundError:
    print("ModuleNotFoundError: Cannot import geo_utils")