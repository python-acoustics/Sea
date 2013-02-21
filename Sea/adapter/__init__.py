"""
The adapter module makes the physics described by the classes in :mod:`Sea.model` available to :term:`FreeCAD`.
Every class in this module has an :attr:`model` attribute, encapsulating the respective class from :mod:`Sea.model`.
"""

from baseclasses import *
from components import *
from system import *
from couplings import *
from excitations import *
from materials import *
from system import *
from object_maps import *
