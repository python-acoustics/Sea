"""
This module extends :term:`FreeCAD` with classes and functions to perform a Statistical Energy Analysis.
"""

import model
import adapter
import actions


import numpy as np
np.seterr(all='raise')