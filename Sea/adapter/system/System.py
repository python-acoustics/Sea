"""
The following System class encapsulates its respective class in :mod:`Sea.system`.
"""
import itertools
import logging
import numpy as np
import FreeCAD as App
import Part

import Sea
from ..base import Base



class System(Base, Sea.model.system.System):
    """
    A class that contains the SEA model
    """
    
    def __init__(self, obj, structure):
        """
        :param obj: FeaturePython object 
        :param group: DocumentObjectGroup that System is part of.
        :param structure: the fused structure which the SEA model will describe.
        """
        
        Base.__init__(self, obj)
        
        obj.addProperty("App::PropertyString", "SeaObject", "SEA", "Type of SEA object.")
        obj.setEditorMode('SeaObject', 1)
        
        obj.addProperty("App::PropertyBool", "Solved", "System", "Boolean showing whether results are present")
        obj.setEditorMode('Solved', 1)
        
        obj.addProperty("App::PropertyLink", "Structure", "System", "Geometry of the structure described by the SEA system.")
        obj.setEditorMode("Structure", 1)
        obj.Structure = structure
        
        
        """Add methods to object"""
        obj.connections = self.connections
        obj.components = self.components
        obj.materials = self.materials
        
        obj.makeComponent = self.makeComponent
        obj.makeMaterial = self.makeMaterial
        obj.makeConnection = self.makeConnection
        obj.addComponentsStructural = self.addComponentsStructural
        obj.addComponentsCavities = self.addComponentsCavities
        obj.addConnections = self.addConnections
        obj.solve = self.solve
        obj.stop = self.stop
        obj.clear = self.clear
        obj.purgeUnusedMaterials = self.purgeUnusedMaterials
        
        
    def onChanged(self, obj, prop):
        """
        Do something when a property has changed.
        
        :param obj: FeaturePython object
        :param prop: Name of property that has changed
        """
        Base.onChanged(self, obj, prop)
        
        #if prop == 'Frequency':
            #for item in obj.Components + obj.Connections:
                #item.Frequency = obj.Frequency
        
    def execute(self, obj):
        """
        Method is executed when doing a recomputation.
        
        :param obj: FeaturePython object
        """
        Base.execute(self, obj)
       
        obj.Solved = obj.Proxy.solved
        
    
    @staticmethod
    def components(obj):
        return filter(Sea.actions.document.isComponent, obj.InList)
        
    @staticmethod
    def materials(obj):
        return filter(Sea.actions.document.isMaterial, obj.InList)
    
    @staticmethod
    def connections(obj):
        return filter(Sea.actions.document.isConnection, obj.InList)
    
    
    @staticmethod
    def makeFrequency(system):
        """
        Make a :class:`Sea.adapter.baseclasses.Frequency` object.
        
        :param system: System
        """
        
        obj = system.Document.addObject("App::FeaturePython", "FrequencySettings")
        Sea.adapter.system.Frequency(obj)
        logging.info("Sea: Created %s.", obj.Name)
        obj.Document.recompute()
        return obj
        
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
        
        obj = system.Document.addObject("App::FeaturePython", 'Component')
        components_map[sort](obj, system, material, part)
        try:
            Sea.adapter.components.ViewProviderComponent(obj.ViewObject)
        except AttributeError:
            pass
        logging.info("Sea: Created %s.", obj.Name)
        #obj.touch()
        system.touch()
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
        
        obj = system.Document.addObject("App::FeaturePython", 'Material')
        try:
            Sea.adapter.materials.ViewProviderMaterial(obj.ViewObject)
        except AttributeError:
            pass
        obj.Label = 'Material' + sort
        materials_map[sort](obj, system)
        logging.info("Sea: Created %s.", obj.Name)
        #obj.touch()
        system.touch()
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
        
        obj = system.Document.addObject("App::FeaturePython", "Connection")
        connections_map[sort](obj, system, components)
        try:
            Sea.adapter.connections.ViewProviderConnection(obj.ViewObject)
        except AttributeError:
            pass
        obj.Label = '' + sort
        logging.info("Sea: Created %s.", obj.Name)
        system.touch()
        obj.Document.recompute()
        return obj  
    
    
    @staticmethod    
    def addComponentsStructural(obj):
        """
        Add all structural components to system.
        
        :param system: an instance of :class:`Sea.adapter.Proxy.System`
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
        
        :param system: an instance of :class:`Sea.adapter.Proxy.System.`

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
        
        :param obj.system: an instance of :class:`Sea.adapter.obj.Proxy.System`
        """
        App.Console.PrintMessage("Adding connections and couplings to the model. This might take a while.\n")
        for component_from, component_to in itertools.combinations(obj.components(), 2):
            
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
        for comp in obj.components():
            comp.Proxy.linked_subsystems = [item.Proxy for item in comp.subsystems()]
            for sub in comp.subsystems():
                subsystems.append(sub.Proxy)
                sub.Proxy.linked_couplings_from = [item.Proxy for item in sub.couplingsFrom()]
                sub.Proxy.linked_couplings_to = [item.Proxy for item in sub.couplingsTo()]
                sub.Proxy.linked_excitations = [item.Proxy for item in sub.excitations()]
        obj.Proxy.subsystems = subsystems
        
        couplings = list()
        for con in obj.connections():
            for coupling in con.couplings():
                couplings.append(coupling.Proxy)
        obj.Proxy.couplings = couplings
        
        
        App.Console.PrintMessage("Solving for modal powers.\n")
        if obj.Proxy.solveSystem():
            App.Console.PrintMessage("Successfully finished solving for the modal powers.\n")
        else:
            App.Console.PrintMessage("Could not solve modal powers.\n")
        obj.Solved = obj.Proxy.solved
        
        
        for component in obj.components():
            component.touch()
            for subsystem in component.subsystems():
                subsystem.touch()
        obj.Document.recompute()
        
    @staticmethod
    def stop(obj):
        """
        Terminate or interrupt the SEA analysis
        
        :param obj: Interrupt calculation of this analysis.
        """
        obj.Proxy.Proxy.stop()
    
    @staticmethod
    def clear(obj):
        """
        Clear results of the SEA analysis
        
        :param obj: SEA model
        """
        obj.Proxy.Proxy.clearResults()
        
    @staticmethod
    def purgeUnusedMaterials(obj):
        """
        Remove all the materials that are not used.
        """
        for material in obj.Materials:
            if not material.Components:
                material.delete()
       
    @staticmethod
    def makeSystem(structure):
        """
        Add :class:`Sea.adapter.system.System` to document`.
        
        :param structure: fused structure the SEA model will describe
        
        """
        system = structure.Document.addObject("App::FeaturePython", "System")
        system.Label = "System"
        Sea.adapter.system.System(system, structure)
        try:
            Sea.adapter.system.ViewProviderSystem(system.ViewObject)
        except AttributeError:
            pass
        frequency = Sea.adapter.system.System.makeFrequency(system)
        system.Frequency = frequency
        system.touch()
        frequency.touch()
        system.Document.recompute()
        return system
        
            