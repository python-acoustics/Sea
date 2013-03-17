"""
Actions related to :class:`FreeCAD.Document`.
"""

import Sea
import Part

import logging

def _isObject(obj, sort):
    """
    Detect whether object is of type sort.
    """
    if isSea(obj):
        if getattr(obj, 'SeaObject') == sort:
            return True
    return False

def isSea(obj):
    """
    Detect whether obj is a SEA object.
    
    :param obj: Object
    
    """
    return True if hasattr(obj, 'SeaObject') else False
    
def isSystem(obj):
    """
    Check whether :attr:`obj` is a :class:`Sea.adapter.system.System`.
    
    :param obj: :class:`FreeCAD.DocumentObject`
    """
    return _isObject(obj, "System")
    
def isComponent(obj):
    """
    Check whether :attr:`obj` is child of :class:`Sea.adapter.baseclasses.Component`.
    
    :param obj: :class:`FreeCAD.DocumentObject`
    """
    return _isObject(obj, "Component")
    
def isConnection(obj):
    return _isObject(obj, "Connection")
    
def isCoupling(obj):
    return _isObject(obj, "Coupling")

def isExcitation(obj):
    return _isObject(obj, "Excitation")
def isMaterial(obj):
    return _isObject(obj, "Material")

def _hasObject(document, sort):
    """
    Detect whether document has any :class:`Sea.adapter.system.System`
    
    :param document: a :attr:`FreeCAD.Document` instance
    :param sort: sort of object
    """
    if document:
        for obj in document.Objects:
            _isObject(obj, sort)
    return False    

def hasComponent(document):
    """
    Check whether document has a child of :class:`Sea.adapter.baseclasses.Component`.
    
    :param document: a :class:`FreeCAD.Document` instance
    """
    return _hasObject(document, 'Component')
    
def hasConnection(document):
    """
    Check whether document has a child of :class:`Sea.adapter.connection.Connection`.
    
    :param document: a :class:`FreeCAD.Document` instance
    """
    return _hasObject(document, 'Connection')

def hasCoupling(document):
    """
    Check whether document has a child of :class:`Sea.adapter.baseclasses.Coupling`.
    
    :param document: a :class:`FreeCAD.Document` instance
    """
    return _hasObject(document, 'Coupling')
    
    
def hasExcitation(document):
    """
    Check whether document has a :class:`Sea.adapter.baseclasses.Excitation`.
    
    :param document: a :class:`FreeCAD.Document` instance
    """
    return _hasObject(document, 'Excitation')
    
def hasMaterial(document):
    """
    Check whether document has a :class:`Sea.adapter.baseclasses.Material`.
    
    :param document: a :class:`FreeCAD.Document` instance
    """
    return _hasObject(document, 'Material')
    
def hasSystem(document):
    """
    Detect whether document has a :class:`Sea.adapter.system.System`
    
    :param document: a :class:`FreeCAD.Document` instance
    """
    return _hasObject(document, 'IsSeaSystem')       
    
def create_empty_system(structure):
    """
    Create a blank SEA model.
    
    :param structure: an instance of :class:`Part.MultiFuse`
    """          
    system = Sea.actions.makeSystem(structure)
    return system
    
def create_system_from_structure(structure):
    """
    Generate an SEA model from a FreeCAD geometry.
    
    :param structure: an instance of :class:`Part.MultiFuse`
    """ 
    system = Sea.actions.factory.makeSystem(structure)
    Sea.actions.system.addComponentsStructural(system)
    Sea.actions.system.addComponentsCavities(system)
    Sea.actions.system.addConnections(system)
    Sea.actions.system.addCouplings(system)
    return system
