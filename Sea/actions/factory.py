"""
The factory contains functions for creating SEA objects in FreeCAD. These functions should not be called directly.
"""

from Sea.adapter.object_maps import *
from Sea.adapter.connection import Connection
from Sea.adapter.system import System

import Sea

import FreeCAD as App
 
import logging
 
def makeComponent(system, part, material, sort):
    """
    Add a component from :mod:`Sea.adapter.components` to an SEA model.
    
    :param system: :class:`Sea.adapter.system.System` to which the component will be added
    :param sort: Type of component specified in :class:`Sea.adapter.components.components_map`
    :param material: Material that the component is made of
    :param part: a :class:`Freecad.Shape` carrying object that the component is based on
        
    """
    obj = system.ComponentsGroup.newObject("App::FeaturePython", 'Component')
    obj.Label = sort
    system.Components = system.Components + [obj]
    components_map[sort](obj, system, material, part)
    logging.info("Sea: Created %s.", obj.Name)
    return obj 
        
    #else:
        #App.Console.PrintWarning("Material and Part do not belong to the same system.")

        
def makeComponentCavity(system, position, sort):
    """
    Add a component from :mod:`Sea.adapter.components` to an SEA model.
    
    :param system: :class:`Sea.adapter.system.System` to which the component will be added
    :param position: a :class:`FreeCAD.Vector` describing the position in the cavity.
    :param sort: Type of component specified in :class:`Sea.adapter.components.components_map`
        
    """
    obj = system.ComponentsGroup.newObject("App::FeaturePython", 'Component')
    obj.Label = sort
    system.Components = system.Components + [obj]
    
    components_map[sort](obj, system, position)
    logging.info("Sea: Created %s.", obj.Name)
    return obj         
        
def makeConnection(system, sort):
    """
    Add a connection to system.
    
    :param system: :class:`Sea.adapter.system.System` to which the connection will be added
    """
    obj = system.ConnectionsGroup.newObject("App::FeaturePython", "Connection")
    obj.Label = sort.capitalize()
    system.Connections = system.Connections + [obj]
    
    Connection(obj, system, sort)
    logging.info("Sea: Created %s.", obj.Name)
    return obj  
        
def makeCoupling(system, connection, component_from, subsystem_from, component_to, subsystem_to, sort):
    """
    Add a coupling to system.
    
    :param connection: an instance of :class:`Sea.adapter.baseclasses.Connection`
    :param component_from: an instance of a child of :class:`Sea.adapter.baseclasses.Component`
    :param subsystem_from: string representing the type of subsystem
    :param component_to: an instance of a child of :class:`Sea.adapter.baseclasses.Component`
    :param subsystem_to: string representing the type of subsystem
    :param sort: sort of coupling as specified in :class:`Sea.adapter.couplings.couplings_map`
    
    """
    #if connection.System == component_from.System == component_to.System:
        
    obj = system.CouplingsGroup.newObject("App::FeaturePython", 'Coupling')
    obj.Label = sort
    system.Couplings = system.Couplings + [obj]
    
    couplings_map[sort](obj, system, connection, component_from, subsystem_from, component_to, subsystem_to)
    logging.info("Sea: Created %s.", obj.Name)
    return obj
    #else:
        #App.Console.PrintWarning("Connection and components do not belong to the same system.")
    
def makeExcitation(system, component, subsystem, sort):
    """
    Add an excitation from :mod:`Sea.adapter.excitations` to the subsystem of component.
    
    :param component: an instance of a child of :class:`Sea.adapter.baseclasses.Component`
    :param subsystem: Subsystem that is excited
    :param sort: Type of excitation specified in :class:`Sea.adapter.excitations.excitations_map`
    
    """
    obj = system.ExcitationsGroup.newObject("App::FeaturePython", 'Excitation')
    obj.Label = sort
    system.Excitations = system.Excitations + [obj]
    
    excitations_map[sort](obj, system, subsystem)
    logging.info("Sea: Created %s.", obj.Name)
    return obj  
    

def makeMaterial(system, sort):
    """
    Add a material from :mod:`Sea.adapter.materials` to SEA system.
    
    :param system: :class:`Sea.adapter.system.System` to which the component will be added
    :param sort: Type of material specified in :class:`Sea.adapter.materials.materials_map`
    """    
    obj = system.MaterialsGroup.newObject("App::FeaturePython", 'Material')
    obj.Label = sort
    system.Excitations = system.Excitations + [obj]
    
    materials_map[sort](obj, system)
    logging.info("Sea: Created %s.", obj.Name)
    return obj    
   
   
def makeSystem(structure):
    """
    Add :class:`Sea.adapter.system.System` to document`.
    
    :param structure: fused structure the SEA model will describe
    
    """    
    sea = structure.Document.addObject("App::DocumentObjectGroup", "SEA")
    
    sea.Label = "SEA model"
    obj = sea.newObject("App::FeaturePython", "System")
    System(obj, sea, structure)
    return obj
    