"""
Module with all components that are available.

The following are Component classes encapsulating their respective :mod:`Sea.model.components` class.

"""

from structural_1D_beam import Component1DBeam
from structural_2D_plate import Component2DPlate
from cavity_3D import Component3DCavity



import inspect, sys
components_map = {item[0]: item[1] for item in inspect.getmembers(sys.modules[__name__], inspect.isclass)}

"""
Dictionary with all available components.
""" 