"""
The following dictionaries provide easy access to the objects described in this module.
"""


from components import *
from subsystems import *
from couplings import *
from excitations import *
from materials import *

#from collections import namedtuple


#ObjectsMap = namedtuple('ObjectsMap', ['name', 'description', 'obj'])


#components_map = {
    #'beam' : ObjectsMap('Beam', 'A one-dimensional structural component.', ComponentBeam),
    #}
    
#subsystems_map = {
    #'long' : ObjectsMap('Subsystem longitudinal waves', 'A subsystem for longitudinal waves in structural components.', SubsystemLong),
    #'bend' : ObjectsMap('Subsystem bending waves', 'A subsystem for bending or flexural waves in structural components.', SubsystemBend),
    #'shear' : ObjectsMap('Subsystem shear waves', 'A subsystem for shear waves in structural components.', SubsystemShear),
    #'cavity2d' : ObjectsMap('Subsystem 2D cavity', 'A subsystem for a 2-dimensional cavity.', SubsystemCavity2D),
    #'cavity3d' : ObjectsMap('Subsystem 3D cavity', 'A subsystem for a 3-dimensional cavity.', SubsystemCavity3D),
    #}  
    
#couplings_map = {
    #'junction' : ObjectsMap('Junction coupling', 'A one-dimensional coupling (point/junction).', CouplingJunction),
    #}
    
#excitations_map = {
    #'rain' : ObjectsMap('Rain on the roof excitation.', 'A rain on the roof excitation.', ExcitationRain),
    #}
    
#materials_map = {
    #'solid' : ObjectsMap('Solid material', 'A solid material.', MaterialSolid),
    #}

    
objects_map = {
    'component' : components_map,
    'subsystem' : subsystems_map,
    'coupling' : couplings_map,
    'excitation' : excitations_map,
    'material' : materials_map,
    }
    
    