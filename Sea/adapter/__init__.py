"""
The adapter module makes the physics described by the classes in :mod:`Sea.model` available to :term:`FreeCAD`.
Every class in this module has an :attr:`model` attribute, encapsulating the respective class from :mod:`Sea.model`.
"""


import base
import components
import connections
import system
import couplings
import excitations
import materials
import object_maps
