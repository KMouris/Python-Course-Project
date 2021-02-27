"""Basic imports and functions for geo_utils"""
try:
    import logging
    import glob
    import os
    import urllib
    import subprocess
    import itertools
    import shutil
except ImportError as e:
    raise ImportError("Could not import standard libraries:\n{0}".format(e))

# import scientific python packages
try:
    import numpy as np
    # import matplotlib  # for future use
except ImportError as e:
    raise ImportError("Could not import numpy/matplotlib (is it installed?). {0}".format(e))
try:
    import pandas as pd
except ImportError as e:
    raise ImportError("Could not import pandas (is it installed?). {0}".format(e))

# import osgeo python packages
try:
    import gdal
    import osr
    from gdal import ogr
except ImportError as e:
    raise ImportError("Could not import gdal and dependent packages (is it installed?). {0}".format(e))

# import other geospatial python packages
try:
    import geopandas
except ImportError as e:
    raise ImportError("Could not import geopandas (is it installed?). {0}".format(e))
try:
    import alphashape
except ImportError as e:
    raise ImportError("Could not import alphashape (is it installed?). {0}".format(e))
try:
    import shapely
    from shapely.geometry import Polygon, LineString, Point
except ImportError as e:
    raise ImportError("Could not import shapely (is it installed?). {0}".format(e))
try:
    import fiona
except ImportError as e:
    raise ImportError("Could not import fiona (is it installed?). {0}".format(e))
try:
    # install pyshp to enable shapefile import
    import shapefile
except ImportError as e:
    raise ImportError("Could not import pyshp (shapefile - is it installed?). {0}".format(e))
try:
    import geojson
except ImportError as e:
    raise ImportError("Could not import fiona (is it installed?). {0}".format(e))

# Global variables
cache_folder = os.path.abspath("") + "/__cache__/"
nan_value = -9999.0

gdal_dtype_dict = {
    0: "gdal.GDT_Unknown",
    1: "gdal.GDT_Byte",
    2: "gdal.GDT_UInt16",
    3: "gdal.GDT_Int16",
    4: "gdal.GDT_UInt32",
    5: "gdal.GDT_Int32",
    6: "gdal.GDT_Float32",
    7: "gdal.GDT_Float64",
    8: "gdal.GDT_CInt16",
    9: "gdal.GDT_CInt32",
    10: "gdal.GDT_CFloat32",
    11: "gdal.GDT_CFloat64",
}


def cache(fun):
    """Makes a function running in a temoprary ``__cache__`` sub-folder to enable deleting temporary trash files."""
    def wrapper(*args, **kwargs):
        check_cache()
        fun(*args, **kwargs)
        remove_directory(cache_folder)
    wrapper.__doc__ = fun.__doc__
    return wrapper


def check_cache():
    """Creates the cache folder if it does not exist."""
    try:
        os.makedirs(cache_folder)
    except OSError:
        pass

def remove_directory(directory):
    """Removes a directory and all its contents - be careful!

    Args:
        directory (str): directory to remove (delete)

    Returns:
        None: Deletes directory.
    """
    try:
        for root, dirs, files in os.walk(directory):
            for f in files:
                os.unlink(os.path.join(root, f))
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))
        shutil.rmtree(directory)
    except PermissionError:
        print("WARNING: Could not remove %s (files locked by other program)." % directory)
    except FileNotFoundError:
        print("WARNING: The directory %s does not exist." % directory)
    except NotADirectoryError:
        print("WARNING: %s is not a directory." % directory)
