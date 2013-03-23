"""
The following System class encapsulates its respective class in :mod:`Sea.model.system`.
"""

import Sea

import logging
import FreeCAD as App

import numpy as np

class System(object):
    """
    A class that contains the SEA model
    """
    
    model = Sea.model.system.System()
    
    
    _components = list()
    _connections = list()
    _couplings = list()
    _excitations = list()
    _materials = list()
    
    
    def __init__(self, obj, group, structure):
        """
        :param obj: FeaturePython object 
        :param group: DocumentObjectGroup that System is part of.
        :param structure: the fused structure which the SEA model will describe.
        """

        self.model = Sea.model.system.System()
        
        #obj.addProperty("App::PropertyLinkList","Objects","Objects", "Objects linked to SEA System")
        obj.addProperty("App::PropertyLinkList","Parts","Objects", "Parts linked to SEA System")
        obj.addProperty("App::PropertyLinkList","Components","Objects", "Components linked to SEA System")
        obj.addProperty("App::PropertyLinkList","Connections","Objects", "Connections linked to SEA System")
        #obj.addProperty("App::PropertyLinkList","Couplings","Objects", "Couplings linked to SEA System")
        obj.addProperty("App::PropertyLinkList","Excitations","Objects", "Couplings linked to SEA System")
        obj.addProperty("App::PropertyLinkList","Materials","Objects", "Materials linked to SEA System")
        
        obj.addProperty("App::PropertyString", "SeaObject", "SEA", "Type of SEA object.")
        
        obj.addProperty("App::PropertyFloatList", "Frequency", "System","List of available frequency bands")
        
        obj.addProperty("App::PropertyIntegerList", "EnabledBands", "System","List of enabled frequency bands")
        
        obj.addProperty("App::PropertyBool", "Octaves", "System", "Use 1/1-octaves (True) or 1/3-octaves (False).")        
        obj.addProperty("App::PropertyBool", "Solved", "System", "Boolean showing whether results are present")
        
        obj.addProperty("App::PropertyLink", "Structure", "System", "Geometry of the structure described by the SEA system.")
        obj.Structure = structure
        
        
        obj.Proxy = self
               
        obj.SeaObject = 'System'
        
        """
        Create DocumentGroups for SEA objects
        """
        
        
        obj.addProperty("App::PropertyLink", "ComponentsGroup", "Groups", "Components that are part of System.")
        obj.addProperty("App::PropertyLink", "ConnectionsGroup", "Groups", "Connections that are part of System.")
        obj.addProperty("App::PropertyLink", "ExcitationsGroup", "Groups", "Excitations that are part of System.")
        obj.addProperty("App::PropertyLink", "MaterialsGroup", "Groups", "Materials that are part of System.")
        
        #obj.addProperty("App::PropertyLink", "ComponentsStructuralGroupGroup", "Groups", "Structural components that are part of System.")
        #obj.addProperty("App::PropertyLink", "ComponentsCavityGroup", "Groups", "Cavity components that are part of System.")
        
        obj.ComponentsGroup = group.newObject("App::DocumentObjectGroup", "GroupComponents")
        obj.ComponentsGroup.Label = "Components"
        
        #obj.ComponentsStructuralGroup = obj.ComponentsGroup.newObject("App::DocumentObjectGroup", "GroupComponentsStructural")
        #obj.ComponentsStructuralGroup.Label = "Structural"
        
        #obj.ComponentsCavityGroup = obj.ComponentsGroup.newObject("App::DocumentObjectGroup", "GroupComponentsCavity")
        #obj.ComponentsStructuralGroup.Label = "Cavities"
        
        obj.ConnectionsGroup = group.newObject("App::DocumentObjectGroup", "GroupConnections")
        obj.ConnectionsGroup.Label = "Connections"
        
        obj.ExcitationsGroup = group.newObject("App::DocumentObjectGroup", "GroupExcitations")
        obj.ExcitationsGroup.Label = "Excitations"    
        
        obj.MaterialsGroup = group.newObject("App::DocumentObjectGroup", "GroupMaterials")
        obj.MaterialsGroup.Label = "Materials"    
        
        self.execute(obj)
        
    def onChanged(self, obj, prop):
        """
        Do something when a property has changed.
        
        :param obj: FeaturePython object
        :param prop: Name of property that has changed
        """
        
        logging.info("Object %s - onChanged - Changing property %s.", obj.Name, prop)
  
        if prop == 'Octaves':
            self.model.octaves = obj.Octaves
            
            self.model.enabled_bands = map(bool, np.array(obj.EnabledBands))
            obj.EnabledBands = map(int, list(self.model.enabled_bands))

        elif prop == 'EnabledBands':
            self.model.enabled_bands = map(bool, np.array(obj.EnabledBands))
    
        elif prop == 'Frequency':
            self.model.frequency = np.array(obj.Frequency)
            for item in obj.Components + obj.Connections:
                item.Frequency = obj.Frequency
        
    def execute(self, obj):
        """
        Method is executed when doing a recomputation.
        
        :param obj: FeaturePython object
        """
        logging.info("Object %s - execute - Executing..")

        obj.Frequency = map(float, list(self.model.frequency))
        
        obj.Solved = self.model.solved
        obj.Octaves = self.model.octaves
        obj.EnabledBands = map(int, list(self.model.enabled_bands))
        
        #self.update_objects_lists(obj)

        
   
    
    #def update_objects_lists(self, obj):
        #"""
        #Update the objects lists of the SEA model.
        #"""
        
        #App.Console.PrintMessage("Updating System lists.")
        
        #components = list()
        #connections = list()
        #couplings = list()
        #excitations = list()
        #materials = list()
        
        #components_proxy = list()
        #connections_proxy = list()
        #couplings_proxy = list()
        #excitations_proxy = list()
        #materials_proxy = list()
        
        #for item in obj.InList:
            #if Sea.actions.document.isComponent(item):
                #components.append(item)
                #components_proxy.append(item.Proxy.model)
            #elif Sea.actions.document.isConnection(item):
                #connections.append(item)
                #connections_proxy.append(item.Proxy.model)
            #elif Sea.actions.document.isCoupling(item):
                #couplings.append(item)
                #couplings_proxy.append(item.Proxy.model)
            #elif Sea.actions.document.isExcitation(item):
                #excitations.append(item)
                #excitations_proxy.append(item.Proxy.model)
            #elif Sea.actions.document.isMaterial(item):
                #couplings.append(item.Proxy.model)
                    
        #self.model.components = components_proxy
        #self.model.connections = connections_proxy
        #self.model.couplings = couplings_proxy
        #self.model.excitations = excitations_proxy
        #self.model.materials = materials_proxy
        #self.model.objects = components_proxy + connections_proxy + couplings_proxy + excitations_proxy + materials_proxy
        
        #obj.Components = components
        #obj.Connections = connections
        #obj.Couplings = couplings
        #obj.Excitations = excitations
        #obj.Materials = materials
        #obj.Objects = components + connections + couplings + excitations + materials
        
    #@property
    #def components(self):
        #return self._components
    
    #@property
    #def connections(self):
        #return self._connections
        
    #@property
    #def couplings(self):
        #return self._couplings
        
    #@property
    #def excitations(self):
        #return self._excitations
        
    #@property
    #def materials(self):
        #return self._materials
        
    #def _objects_list(self, sort):
        #"""Create a list of objects of type sort that refer to this object."""
        #return [item for item in system.InList if Sea.actions.connection._isObject(item, sort)]

    #def components_list(self):
        #return _objects_list('Component')

    #def connections_list(self):
        #return _objects_list('Connection')
        
    #def connections_list(self):
        #return _objects_list('Connection')    