"""
The factory contains functions for creating SEA objects in FreeCAD.

"""

from Sea.adapter.object_maps import *

from Sea.adapter.system import System

import Sea

import FreeCAD as App
 
 
 
def makeComponent(sort, system=None, material=None, part=None, **properties):
    """Add a component to an SEA model.
    
    :param system: System to which the component will be added
    :param sort: Type of component to be added
    :param material: Material that the component is made of
    :param part: Part that this component is based on
    :param **properties: Optional properties
    
    """
    
    if system:
        document = system.Document
    elif App.ActiveDocument:
        document = App.ActiveDocument
    else:
        App.newDocument()
        document = App.ActiveDocument
        
    obj = document.addObject("App::FeaturePython", sort)
    components_map[sort](obj, system, material, part, **properties)
    
    #Sea.adapter.baseclasses.ViewProviderBaseClass(obj.ViewObject)
    logging.info("Sea: Created %s.", obj.Name)
    return obj 
    

def makeSubsystem(sort, system=None, component=None, **properties):
    """
    Add a subsystem to system.
    
    :param system: System to which the coupling will be added
    :param sort: Type of coupling to be added
    :param component: Component this subsystem is based on
    :param **properties: Optional properties
    """
    if system:
        document = system.Document
    elif App.ActiveDocument:
        document = App.ActiveDocument
    else:
        App.newDocument()
        document = App.ActiveDocument
        
    obj = document.addObject("App::FeaturePython", sort)
    subsystems_map[sort](obj, system, component, **properties)
    logging.info("Sea: Created %s.", obj.Name)
    return obj       
    
def makeCoupling(sort, system=None, subsystem_from=None, subsystem_to=None, **properties):
    """Add a coupling to system.
    
    :param system: System to which the coupling will be added
    :param sort: Type of coupling to be added
    :param subsystem_from: Subsystem coupling begins
    :param subsystem_to: Subsystem coupling ends
    :param **properties: Optional properties
    """
    if system:
        document = system.Document
    elif App.ActiveDocument:
        document = App.ActiveDocument
    else:
        App.newDocument()
        document = App.ActiveDocument
        
    obj = document.addObject("App::FeaturePython", sort)
    couplings_map[sort](obj, system, subsystem_from, subsystem_to, **properties)
    logging.info("Sea: Created %s.", obj.Name)
    return obj  
    
def makeExcitation(sort, system=None, subsystem=None, **properties):
    """
    Add an excitation to system
    
    :param system: System to which the excitation will be added
    :param sort: Type of excitation to be added
    :param subsystem: Subsystem that is excited
    :param **properties: Optional properties
    """
    if system:
        document = system.Document
    elif App.ActiveDocument:
        document = App.ActiveDocument
    else:
        App.newDocument()
        document = App.ActiveDocument
        
    obj = document.addObject("App::FeaturePython", sort)
    excitations_map[sort](obj, system, subsystem, **properties)
    logging.info("Sea: Created %s.", obj.Name)
    return obj  
    

def makeMaterial(sort, system=None, **properties):
    """Add material to SEA system.
    
    :param system: System to which the material will be added
    :param sort: Type of material to be added
    :param **properties: Optional properties
    """
    if system:
        document = system.Document
    elif App.ActiveDocument:
        document = App.ActiveDocument
    else:
        App.newDocument()
        document = App.ActiveDocument
        
    obj = document.addObject("App::FeaturePython", sort)
    materials_map[sort](obj, system, **properties)
    logging.info("Sea: Created %s.", obj.Name)
    return obj    
   
   
def makeSystem(document):
    """
    Add System to document
    
    :param document: Document to which the System will be added
    """
    #from FreeCAD import Document
        
    if document.Type == "App::Document":
        obj = document.addObject("App::FeaturePython", "System")
    elif document.Type == "App::DocumentObjectGroup":
        obj = document.newObject("App::FeaturePython", "System")
    else:
        TypeError("Object is neither Document nor DocumentObjectGroup")
    System(obj)
    return obj