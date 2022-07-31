"""
This module provides bindings to C/C++ functions defined by OpenMC shared
library. When the :mod:`openmc.lib` package is imported, the OpenMC shared
library is automatically loaded. Calls to the OpenMC library can then be via
functions or objects in :mod:`openmc.lib`, for example:

.. code-block:: python

    openmc.lib.init()
    openmc.lib.run()
    openmc.lib.finalize()

"""

from ctypes import CDLL, c_bool, c_int
from ctypes.util import find_library
import os
import sys

import pkg_resources

if os.environ.get('READTHEDOCS', None) != 'True':
    # Open shared library
    if  sys.platform == 'win32':
        _lib = find_library('libopenmc')
        try:
            _dll = CDLL(_lib)
        except FileNotFoundError:
            # Python >= 3.8
            os.add_dll_directory(os.path.dirname(_lib))
    elif sys.platform == 'darwin':
        _lib = find_library('openmc')
        _dll = CDLL(_lib)
    else:
        _lib = find_library('openmc')
        _filename = pkg_resources.resource_filename(
            __name__, _lib)
        _dll = CDLL(_filename)
else:
    # For documentation builds, we don't actually have the shared library
    # available. Instead, we create a mock object so that when the modules
    # within the openmc.lib package try to configure arguments and return
    # values for symbols, no errors occur
    from unittest.mock import Mock
    _dll = Mock()


def _dagmc_enabled():
    return c_bool.in_dll(_dll, "DAGMC_ENABLED").value

def _coord_levels():
    return c_int.in_dll(_dll, "n_coord_levels").value

def _libmesh_enabled():
    return c_bool.in_dll(_dll, "LIBMESH_ENABLED").value

from .error import *
from .core import *
from .nuclide import *
from .material import *
from .cell import *
from .mesh import *
from .filter import *
from .tally import *
from .settings import settings
from .math import *
from .plot import *

# Flag to denote whether or not openmc.lib.init has been called
# TODO: Establish and use a flag in the C++ code to represent the status of the
# openmc_init and openmc_finalize methods
is_initialized = False
