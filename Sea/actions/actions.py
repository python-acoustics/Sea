"""
The following are some actions which are available.
"""



import FreeCAD as App
import Part

import Sea

import logging


def _hasObject(document, sort):
    """
    Detect whether document has any :class:`Sea.adapter.system.System`
    """
    if document:
        for item in document.Objects:
            if hasattr(item, sort):
                if getattr(item, sort) is True:
                    return True
    return False    
    

def hasComponent(document):
    """
    Check whether document has a child of :class:`Sea.adapter.baseclasses.Component`.
    """
    return _hasObject(document, 'IsSeaComponent')
    
def hasSubsystem(document):
    """
    Check whether document has a child of :class:`Sea.adapter.baseclasses.Subsystem`.
    """
    return _hasObject(document, 'IsSeaSubsystem')

def hasCoupling(document):
    """
    Check whether document has a child of :class:`Sea.adapter.baseclasses.Subsystem`.
    """
    return _hasObject(document, 'IsSeaCoupling')
    
def hasExcitation(document):
    """
    Check whether document has a :class:`Sea.adapter.baseclasses.Excitation`.
    """
    return _hasObject(document, 'IsSeaExcitation')
    
def hasMaterial(document):
    """
    Check whether document has a :class:`Sea.adapter.baseclasses.Material`.
    """
    return _hasObject(document, 'IsSeaMaterial')
    
def hasSystem(document):
    """
    Detect whether document has a :class:`Sea.adapter.system.System`
    """
    return _hasObject(document, 'IsSeaSystem')       
    

def create_empty_system(document):
    """
    Create new SEA analysis
    
    :param document: Document to which to add the model.
    """  
 
    SEA_group = document.addObject("App::DocumentObjectGroup", "SEA")
    SEA_group.Label = "SEA model"        
    system = Sea.actions.makeSystem(document)
    SEA_group.addObject(system)
    
    return system

    
def create_system_from_document(document):
    """
    Construct an SEA model from a FreeCAD model.
    
    :param document: Document to which to add the model.
    
    """ 
        
    SEA_group = document.addObject("App::DocumentObjectGroup", "SEA")
    SEA_group.Label = "SEA model"        
    system = Sea.actions.makeSystem(document)
    SEA_group.addObject(system)
    
    components_group = SEA_group.newObject("App::DocumentObjectGroup", "Components")
    components_group.Label = "Components"
    
    subsystems_group = SEA_group.newObject("App::DocumentObjectGroup", "Subsystems")
    subsystems_group.Label = "Subsystems"
    
    couplings_group = SEA_group.newObject("App::DocumentObjectGroup", "Couplings")
    couplings_group.Label = "Couplings"
    
    excitations_group = SEA_group.newObject("App::DocumentObjectGroup", "Excitations")
    excitations_group.Label = "Excitations"    
    
    materials_group = SEA_group.newObject("App::DocumentObjectGroup", "Materials")
    materials_group.Label = "Materials"       
    
    # Create a component for every Object/Part
    # Only works for structural components. Cavities have to be added manually for now. (Can use Material type to detect whether it is a cavity?)
    for obj in document.Objects:
        if isinstance(obj, Part.Feature):
            part = obj
            logging.info("object is part feature\n")
            #component_type = determine_component_type(item) # returns None if no applicable component_type could be found
            
            properties = None
            sort = determine_component_sort(part)

            material = Sea.actions.makeMaterial('MaterialSolid', system)
            materials_group.addObject(material)
            component = Sea.actions.makeComponent(sort, system, material, part)
            components_group.addObject(component)
            
            subsys_long = Sea.actions.makeSubsystem('SubsystemLong', system, component)
            subsystems_group.addObject(subsys_long)
            subsys_bend = Sea.actions.makeSubsystem('SubsystemBend', system, component)
            subsystems_group.addObject(subsys_bend)
            
            #makeSubsystem(system, 'shear', component)
            
            #if not None:
                #component_label = 
                #system1.addComponent()
                
                
                ##if structural:
                #system1.addSubSystem(label, 'long', [], component_label)
                #system1.addSubSystem(label, 'bend', [], component_label)
                #system1.addSubSystem(label, 'shear', [], component_label)
        
    return system

    
    # Components and subsystems have been added. Now add couplings. Use Shape Common on every Component combination to detect whether there is a coupling.
    
        
    
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


def determine_component_sort(part):
    """
    Determine which component describes the Part best
    
    :param part: Part to be investigated
    """
    return 'beam'
    
def detect_if_coupled(shell1, shell2):
    """
    Check if the shells have a common or not.
    
    :param shell1: Shell A
    :param shell2: Shell B
    
    Returns True or False depending on whether the shells have a common shell or not.
    """
    
    common = shell1.common(shell2)
    return bool(common.shells)
    
    

def create_couplings(system, documentgroup, obj1, obj2):
    
    #for solid1 in obj1.Part.Shape.Solids:
        #for solid2 in obj2.Part.Shape.Shells:
            #common = solid1.common(solid2)
            #if bool(common.solids):
                #"""If the components have a solid (volume) in common..."""
                #for subsystem_a in obj1.LinkedSubsystems:
                    #for subsystem_b in obj2.LinkedSubsystems:
                        #coupling = makeCoupling(system, 'volume', obj1, obj2)
                        #documentgroup.addObject(coupling)
                        #coupling = makeCoupling(system, 'volume', obj2, obj1)
                        #documentgroup.addObject(coupling)   
    
    for shell1 in obj1.Part.Shape.Shells:
        for shell2 in obj2.Part.Shape.Shells:
            common = shell1.common(shell2)
            if bool(common.shells):
                """If the components have a shell (surface) in common..."""
                for subsystem_a in obj1.LinkedSubsystems:
                    for subsystem_b in obj2.LinkedSubsystems:
                        coupling = makeCoupling(system, 'surface', obj1, obj2)
                        documentgroup.addObject(coupling)
                        coupling = makeCoupling(system, 'surface', obj2, obj1)
                        documentgroup.addObject(coupling)
                    