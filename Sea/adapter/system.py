"""
The following System class encapsulates its respective class in :mod:`Sea.model.system`.
"""

import FreeCAD as App
import Part
import Sea
from baseclasses.baseclass import BaseClass


import itertools
import logging
import numpy as np



class System(BaseClass):
    """
    A class that contains the SEA model
    """
    
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
        model = Sea.model.system.System
        BaseClass.__init__(self, obj, model)
        
        obj.addProperty("App::PropertyPythonObject", "Model", "Base", "Model describing the object.")
        
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
        
        """Add methods to object"""
        obj.makeComponent = self.makeComponent
        obj.makeMaterial = self.makeMaterial
        obj.makeConnection = self.makeConnection
        obj.addComponentsStructural = self.addComponentsStructural
        obj.addComponentsCavities = self.addComponentsCavities
        obj.addConnections = self.addConnections
        obj.solve = self.solve
        obj.stop = self.stop
        obj.clear = self.clear
        
        
    def onChanged(self, obj, prop):
        """
        Do something when a property has changed.
        
        :param obj: FeaturePython object
        :param prop: Name of property that has changed
        """
        BaseClass.onChanged(self, obj, prop)
        
        if prop == 'Octaves':
            obj.Model.octaves = obj.Octaves
            
            obj.Model.enabled_bands = map(bool, np.array(obj.EnabledBands))
            obj.EnabledBands = map(int, list(obj.Model.enabled_bands))

        elif prop == 'EnabledBands':
            obj.Model.enabled_bands = map(bool, np.array(obj.EnabledBands))
    
        elif prop == 'Frequency':
            obj.Model.frequency = np.array(obj.Frequency)
            for item in obj.Components + obj.Connections:
                item.Frequency = obj.Frequency
        
    def execute(self, obj):
        """
        Method is executed when doing a recomputation.
        
        :param obj: FeaturePython object
        """
        BaseClass.execute(self, obj)
        obj.Frequency = map(float, list(obj.Model.frequency))
        
        obj.Solved = obj.Model.solved
        obj.Octaves = obj.Model.octaves
        obj.EnabledBands = map(int, list(obj.Model.enabled_bands))
        
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
                #components_proxy.append(item.Model)
            #elif Sea.actions.document.isConnection(item):
                #connections.append(item)
                #connections_proxy.append(item.Model)
            #elif Sea.actions.document.isCoupling(item):
                #couplings.append(item)
                #couplings_proxy.append(item.Model)
            #elif Sea.actions.document.isExcitation(item):
                #excitations.append(item)
                #excitations_proxy.append(item.Model)
            #elif Sea.actions.document.isMaterial(item):
                #couplings.append(item.Model)
                    
        #obj.Model.components = components_proxy
        #obj.Model.connections = connections_proxy
        #obj.Model.couplings = couplings_proxy
        #obj.Model.excitations = excitations_proxy
        #obj.Model.materials = materials_proxy
        #obj.Model.objects = components_proxy + connections_proxy + couplings_proxy + excitations_proxy + materials_proxy
        
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
        

    @staticmethod
    def makeComponent(system, sort, material, part):
        """
        Add a component from :mod:`Sea.adapter.components` to an SEA model.
        
        For structural components, part is a :class:`Freecad.Part` that the component is based on.
        For cavities, part is a :class:`FreeCAD.Vector` describing the position in the cavity.    
        
        :param system: a instance of :class:`Sea.adapter.system.System` to which the component will be added.
        :param sort: type of component as specified in :class:`Sea.adapter.components.components_map`
        :param material: an instance of a child of :class:`Sea.adapter.baseclasses.Material` that the component is made of.
        :param part: an instance of :class:`Freecad.Part` that the component is based on.
        :param position: a :class:`FreeCAD.Vector` describing the position in the cavity.    
        """
        from Sea.adapter.object_maps import components_map
        
        obj = system.ComponentsGroup.newObject("App::DocumentObjectGroupPython", 'Component')
        components_map[sort](obj, system, material, part)
        logging.info("Sea: Created %s.", obj.Name)
        obj.Document.recompute()
        return obj 

    @staticmethod
    def makeMaterial(system, sort):
        """
        Add a material from :mod:`Sea.adapter.materials` to SEA system.
        
        :param system: :class:`Sea.adapter.system.System` to which the component will be added
        :param sort: Type of material specified in :class:`Sea.adapter.materials.materials_map`
        """ 
        from Sea.adapter.object_maps import materials_map
        
        obj = system.MaterialsGroup.newObject("App::FeaturePython", 'Material')
        #obj.Label = sort
        materials_map[sort](obj, system)
        logging.info("Sea: Created %s.", obj.Name)
        obj.Document.recompute()
        return obj

    @staticmethod
    def makeConnection(system, sort, components):
        """
        Add a connection to system.
        
        :param system: :class:`Sea.adapter.system.System` to which the connection will be added
        :param sort: sort
        :param components: list of components
        """
        from Sea.adapter.object_maps import connections_map
        
        obj = system.ConnectionsGroup.newObject("App::DocumentObjectGroupPython", "Connection")
        connections_map[sort](obj, system, components)
        logging.info("Sea: Created %s.", obj.Name)
        obj.Document.recompute()
        return obj  
    
    
    @staticmethod    
    def addComponentsStructural(obj):
        """
        Add all structural components to system.
        
        :param system: an instance of :class:`Sea.adapter.Model.System`
        """
        
        App.Console.PrintMessage("Adding structural components to the model.\n")
        for part in obj.Structure.Shapes:
            if isinstance(part, Part.Feature):
                sort = Sea.actions.component.determine_structural_sort(part)
                if sort:
                    material = obj.makeMaterial('MaterialSolid')
                    obj.makeComponent(sort, material, part)
    
        obj.Document.recompute()
        App.Console.PrintMessage("Finished adding structural components to the model.\n")
        
    @staticmethod
    def addComponentsCavities(obj):
        """
        Add all cavity components to system.
        
        :param system: an instance of :class:`Sea.adapter.Model.System.`

        """
        
        """Add cavity components"""
        """These are given by every negative shell volume in the structure."""
        App.Console.PrintMessage("Adding cavity components to the model.\n")
        for shape in obj.Structure.Shape.Shells:
            if shape.Volume < 0.0:
                pos = shape.BoundBox.Center
                sort = Sea.actions.component.determine_cavity_sort(shape)
                if sort:
                    material = obj.makeMaterial('MaterialGas')
                    obj.makeComponent(sort, material, pos)
    
        obj.Document.recompute()
        App.Console.PrintMessage("Finished adding cavity components to the model.\n")
    
    #connection_options = {
        ## Component from and component to
        #('Component1DBeam', 'Component1DBeam') : {  # How are they connected
                                                  #('Short', 'Short') : 'Point',   # Which connection type
                                                  #('Long', 'Long') : 'Line',
                                                    #}
        #('Component2DPlate', 'Component2DPlate') : {  # How are they connected
                                                  #('Short', 'Short') : 'Line',   # Which connection type
                                                  #('Long', 'Long') : 'Surface',
                                                    #}
        
        
        #}
    
    @staticmethod
    def determineConnectionSort(comp_from, comp_to):
        
        if Sea.actions.connection.ShapeConnection(comp_from.Shape, comp_to.Shape).commons():
            try:
                options = {
                    ('Component2DPlate', 'Component2DPlate') : ['ConnectionLine'],
                    ('Component2DPlate', 'Component3DCavity') : ['ConnectionSurface'],
                    ('Component3DCavity', 'Component2DPlate') : ['ConnectionSurface'],
                    
                    }
                
                return options[(comp_from.ClassName, comp_to.ClassName)]
            except KeyError:
                return []
        return []
    
    @staticmethod
    def addConnections(obj):
        """
        Detect whether connections exist between the Components in the System. If so, add the Connections and Couplings.
        
        :param obj.system: an instance of :class:`Sea.adapter.obj.Model.System`
        """
        App.Console.PrintMessage("Adding connections and couplings to the model. This might take a while.\n")
        for component_from, component_to in itertools.combinations(obj.Components, 2):
            connections = System.determineConnectionSort(component_from, component_to)
            
            for sort in connections:
                obj.makeConnection(sort, [component_from, component_to])
        obj.Document.recompute()    
        App.Console.PrintMessage("Finished adding connections and couplings to the model.\n")
               
    @staticmethod
    def solve(obj):
        """
        Perform the SEA analysis.
        
        :param obj: Perform SEA analysis on this model.
        """
        
        subsystems = list()
        for comp in obj.Components:
            for sub in comp.Subsystems:
                subsystems.append(sub.Model)
        obj.Model.subsystems = subsystems
        
        couplings = list()
        for con in obj.Connections:
            for coupling in con.Couplings:
                couplings.append(coupling.Model)
        obj.Model.couplings = couplings
        
        
        App.Console.PrintMessage("Solving for modal powers.\n")
        obj.Model.solveSystem()
        App.Console.PrintMessage("Finished solving for the modal powers.\n")
        
        for component in obj.Components:
            for subsystem in component.Subsystems:
                subsystem.touch()
        obj.Document.recompute()
        
    @staticmethod
    def stop(obj):
        """
        Terminate or interrupt the SEA analysis
        
        :param obj: Interrupt calculation of this analysis.
        """
        obj.Model.Proxy.stop()
    
    @staticmethod
    def clear(obj):
        """
        Clear results of the SEA analysis
        
        :param obj: SEA model
        """
        obj.Model.Proxy.clearResults()
        
    