"""
Actions related to :class:`Sea.adapter.system.System`.
"""

import Sea
import Part

import logging
import itertools

import FreeCAD as App


class System(object):
    """
    Class with public methods to manipulate :class:`Sea.adapter.system.System`.
    """
    
    def __init__(self, obj):
        
        
        if Sea.actions.document.isSystem(obj):
            self.system = obj
        else:
            App.Console.PrintError('Invalid DocumentObject.\n')
            raise ValueError

    def addComponentsStructural(self):
        """
        Add all structural components to system.
        
        :param system: an instance of :class:`Sea.adapter.system.System`
        """
        
        App.Console.PrintMessage("Adding structural components to the model.\n")
        for part in self.system.Structure.Shapes:
            if isinstance(part, Part.Feature):
                sort = Sea.actions.component.determine_structural_sort(part)
                if sort:
                    material = Sea.actions.factory.makeMaterial(self.system, 'MaterialSolid')
                    Sea.actions.factory.makeComponent(self.system, sort, material, part)
    
        self.system.Document.recompute()
        App.Console.PrintMessage("Finished adding structural components to the model.\n")
        
    def addComponentsCavities(self):
        """
        Add all cavity components to system.
        
        :param system: an instance of :class:`Sea.adapter.system.System.`

        """
        
        """Add cavity components"""
        """These are given by every negative shell volume in the structure."""
        App.Console.PrintMessage("Adding cavity components to the model.\n")
        for shape in self.system.Structure.Shape.Shells:
            if shape.Volume < 0.0:
                pos = shape.BoundBox.Center
                sort = Sea.actions.component.determine_cavity_sort(shape)
                if sort:
                    material = Sea.actions.factory.makeMaterial(self.system, 'MaterialGas')
                    Sea.actions.factory.makeComponentCavity(self.system, sort, material, pos)
    
        self.system.Document.recompute()
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
        
    def addConnections(self):
        """
        Detect whether connections exist between the Components in the Systen. If so, add the Connections and Couplings.
        
        :param self.system: an instance of :class:`Sea.adapter.self.system.System`
        """
        App.Console.PrintMessage("Adding connections and couplings to the model. This might take a while.\n")
        for component_from, component_to in itertools.combinations(self.system.Components, 2):
            connections = self.determineConnectionSort(component_from, component_to)
            
            for sort in connections:
                Sea.actions.factory.makeConnection(self.system, sort, [component_from, component_to])
        self.system.Document.recompute()    
        App.Console.PrintMessage("Finished adding connections and couplings to the model.\n")
               
    def solve(self):
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
        
        #App.Console.PrintMessage(obj)
        
        
        subsystems = list()
        for comp in self.system.Components:
            for sub in comp.Subsystems:
                subsystems.append(sub.Proxy.model)
        self.system.Proxy.model.subsystems = subsystems
        
        couplings = list()
        for con in self.system.Connections:
            for coupling in con.Couplings:
                couplings.append(coupling.Proxy.model)
        self.system.Proxy.model.couplings = couplings
        
        self.system.Proxy.model.solveSystem()
        
            
    def stop(self):
        """
        Terminate or interrupt the SEA analysis
        
        :param obj: Interrupt calculation of this analysis.
        """
        self.system.Proxy.stop()
        
    def clear(self):
        """
        Clear results of the SEA analysis
        
        :param obj: SEA model
        """
        self.system.Proxy.clearResults()
        
        
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
                shape.complement() # Reverse the shape to obtain positive volume
                return shape
            #else:
                #App.Console.PrintWarning("No cavity at this position.\n")
       