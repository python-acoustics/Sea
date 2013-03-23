import abc
import logging
import Sea
import numpy as np
from baseclass import BaseClass

class Coupling(BaseClass):
    """
    Abstract base class for couplings.
    """
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, obj, connection, component_from, subsystem_from, component_to, subsystem_to):
        BaseClass.__init__(self, obj, 'Coupling')
        
        #print connection.ClassName
        connection.Couplings = connection.Couplings + [obj]
        obj.Frequency = connection.Frequency
        
        obj.addProperty("App::PropertyFloatList", "CLF", "Coupling", "Coupling loss factor.")
        
        obj.addProperty("App::PropertyLink", "ComponentFrom", "Coupling", "Component from")
        obj.addProperty("App::PropertyLink", "ComponentTo", "Coupling", "Component to")
        obj.addProperty("App::PropertyLink", "SubsystemFrom", "Coupling", "Subsystem from")
        obj.addProperty("App::PropertyLink", "SubsystemTo", "Coupling", "Subsystem to")
        
        obj.addProperty("App::PropertyFloatList", "ImpedanceFrom", "Subsystem From", "Impedance of connection corrected From subsystem.")     
        obj.addProperty("App::PropertyFloatList", "ResistanceFrom", "Subsystem From", "Resistance of connection corrected From subsystem.")
        
        obj.addProperty("App::PropertyFloatList", "ImpedanceTo", "Subsystem To", "Impedance of connection corrected To subsystem.")
        obj.addProperty("App::PropertyFloatList", "ResistanceTo", "Subsystem To", "Resistance of connection corrected To subsystem.")
        
        
        """How or more specifically, when to update the size of the coupling?"""
        #obj.addProperty("App::PropertyFloat", "Size", "Coupling", "Size of the junction.")
        
        obj.ComponentFrom = component_from
        obj.ComponentTo = component_to
        obj.SubsystemFrom = subsystem_from
        obj.SubsystemTo = subsystem_to
        
    def onChanged(self, obj, prop):
        BaseClass.onChanged(self, obj, prop)
        
        if prop == 'ComponentFrom' or prop == 'SubsystemFrom':
            if obj.ComponentFrom and obj.SubsystemFrom:
                self.model.subsystem_from = obj.SubsystemFrom.Proxy.model
        elif prop == 'ComponentTo' or prop == 'SubsystemTo':
            if obj.ComponentTo and obj.SubsystemTo:
                self.model.subsystem_to = obj.SubsystemTo.Proxy.model
            
            
        
        #pass
        #if prop == 'Connection':
            #self.model.connection = obj.Connection.Proxy.model
        
        #elif prop == 'ComponentFrom' or 'SubsystemFrom':
            #self.model.component_from = Obj.ComponentFrom.Proxy.model
            #self.model.subsystem_from = getattr(Obj.ComponentFrom.Proxy.model, 'subsystem_' + Obj.SubsystemFrom)
            
        #elif prop == 'ComponentTo' or 'SubsystemTo':
            #self.model.component_to = Obj.ComponentTo.Proxy.model
            #self.model.subsystem_to = getattr(Obj.ComponentTo.Proxy.model, 'subsystem_' + Obj.SubsystemTo)
            

    def execute(self, obj):
        BaseClass.execute(self, obj)
        
        obj.CLF = self.model.clf
        
        obj.ImpedanceFrom = map(float, list(self.model.impedance_from))
        obj.ImpedanceTo = map(float, list(self.model.impedance_to))
        obj.ResistanceFrom = map(float, list(self.model.resistance_from))
        obj.ResistanceTo = map(float, list(self.model.resistance_to))
    
    
    #@abc.abstractmethod
    #def size(self, obj):
        #"""
        #Return the size of the coupling.
        #"""
        #return
        