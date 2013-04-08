"""
Module with all components that are available.

The following are Component classes encapsulating their respective :mod:`Sea.model.components` classes.

"""

from Component1DBeam import Component1DBeam
from Component2DPlate import Component2DPlate
from Component3DCavity import Component3DCavity

from ViewProviderComponent import ViewProviderComponent

import inspect, sys
components_map = {item[0]: item[1] for item in inspect.getmembers(sys.modules[__name__], inspect.isclass)}

"""
Dictionary with all available components.
""" 