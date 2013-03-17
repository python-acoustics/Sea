"""
Actions related to :class:`Sea.adapter.system.System`.
"""

import Sea
import Part

import logging
import itertools

import FreeCAD as App

def addComponentsStructural(system):
    """
    Add all structural components to system.
    
    :param system: an instance of :class:`Sea.adapter.system.System`
    """
    for shape in system.Structure.Shapes:
        if isinstance(shape, Part.Feature):
            sort = Sea.actions.component.determine_structural_sort(shape)
            if sort:
                material = Sea.actions.factory.makeMaterial(system, 'MaterialSolid')
                component = Sea.actions.factory.makeComponent(system, shape, material, sort)
    
def addComponentsCavities(system):
    """
    Add all cavity components to system.
    
    :param system: an instance of :class:`Sea.adapter.system.System.`

    """
    
    """Add cavity components"""
    """These are given by every negative shell volume in the structure."""
    for shape in system.Structure.Shape.Shells:
        if shape.Volume < 0.0:
            pos = shape.BoundBox.Center
            sort = Sea.actions.component.determine_cavity_sort(shape)
            if sort:
                Sea.actions.factory.makeComponentCavity(system, pos, sort)
    
def addConnections(system):
    """
    Detect whether connections exist between the Components in the Systen. If so, add the Connections and Couplings.
    
    :param system: an instance of :class:`Sea.adapter.system.System`
    """
    system.Document.recompute()
    
    
    for component_from, component_to in itertools.combinations(system.Components, 2):
        connection_sort = Sea.actions.connection.determineConnectionType(component_from.Shape, component_to.Shape)
        if connection_sort:
            # if both are already in a Connection in connections_list, and they are of the same sort, then don't act.
            x = [True for connection in system.Connections if component_from and component_to in connection.Components and connection.Sort == connection_sort ]
            if any(x):
                """
                This connection already exists.
                """
                pass
            else:
                """
                Connection does not yet exist.
                """
                con = Sea.actions.factory.makeConnection(system, connection_sort)
                Sea.actions.connection.addComponent(con, component_from)
                Sea.actions.connection.addComponent(con, component_to)
        
def addCouplings(system):
    """
    Add all couplings to a system based on the already existing connections.
    
    :param system: an instance of :class:`Sea.adapter.system.System`
    
    """
    for connection in system.Connections:
        Sea.actions.connection.addCouplings(system, connection)
   
def getCavity(structure, position):
    """
    Return shape of cavity in structure for a certain position.
    
    :param structure: a :class:`Part.MultiFuse`
    :param position: a :class:`FreeCAD.Vector`
    """
    tolerance = 0.01
    allowface = False
        
    for shape in structure.Shape.Shells:
        if shape.isInside(position, tolerance, allowface) and shape.Volume < 0.0:
            shape.reverse() # Reverse the shape to obtain positive volume
            return shape
        #else:
            #App.Console.PrintWarning("No cavity at this position.\n")
    
    
    
    
def solve(obj):
    """
    Perform the SEA analysis.
    
    :param obj: Perform SEA analysis on this model.
    """
    
    #print obj.IsSeaSystem
    
    #try:
        #obj = App.ActiveDocument.ActiveObject
        #obj.Proxy.solveSystem()
    #except AttributeError:
        #App.Console.PrintMessage("Please select an SEA System.\n")
    
    App.Console.PrintMessage(obj)
    
    if hasattr(obj, "IsSeaSystem"):
        if obj.IsSeaSystem:
            obj.Proxy.model.solveSystem()
    else:
        App.Console.PrintMessage("Wrong object. Please select an SEA System.\n")

           
def stop(obj):
    """
    Terminate or interrupt the SEA analysis
    
    :param obj: Interrupt calculation of this analysis.
    """
    if obj.IsSeaSystem:
        obj.Proxy.stop()
    else:
        App.Console.PrintMessage("Wrong object. Please select an SEA System.\n")
    
    
def clear(obj):
    """
    Clear results of the SEA analysis
    
    :param obj: SEA model
    """
    if obj.IsSeaSystem:
        obj.Proxy.clearResults()
    else:
        App.Console.PrintMessage("Wrong object. Please select an SEA System.\n")
 
