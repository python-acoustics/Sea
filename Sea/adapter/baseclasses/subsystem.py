import abc
import logging
import Sea
import numpy as np
from baseclass import BaseClass

class Subsystem(BaseClass):
    """
    Abstract base class for all :mod:`Sea.adapter.subsystems` classes.
    """
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, obj, component, model):
        """
        Constructor
        
        :param obj: FreeCAD Python Feature object
        :param component: an instance of a child of :class:`Sea.adapter.baseclasses.Component`
        """
        
        self.model = model()
        self.model.component = component.Proxy.model
        
        BaseClass.__init__(self, obj, 'Subsystem')
        obj.Frequency = component.Frequency
        component.Subsystems = component.Subsystems + [obj]
        
        obj.addProperty("App::PropertyFloatList", "Impedance", "Subsystem", "Impedance")
        obj.addProperty("App::PropertyFloatList", "Resistance", "Subsystem", "Resistance")
        obj.addProperty("App::PropertyFloatList", "Mobility", "Subsystem", "Mobility")
        obj.addProperty("App::PropertyFloatList", "ModalDensity", "Subsystem", "Modal density")
        
        
        obj.addProperty("App::PropertyLinkList", "CouplingsFrom", "Couplings", "Couplings that originate from this subsystem.")
        obj.addProperty("App::PropertyLinkList", "CouplingsTo", "Couplings", "Couplings that end at this subsystem.")
                
    def onChanged(self, obj, prop):
        BaseClass.onChanged(self, obj, prop)
        
        if prop == 'CouplingsFrom':
            #for coupling in obj.CouplingsFrom:
                #coupling.Proxy.model.subsystem_from = self.model
            self.model.linked_couplings_from = [coupling.Proxy.model for coupling in obj.CouplingsFrom]
        if prop == 'CouplingsTo':
            #for coupling in obj.CouplingsTo:
                #coupling.Proxy.model.subsystem_to = self.model        
            self.model.linked_couplings_to = [coupling.Proxy.model for coupling in obj.CouplingsTo]

    def execute(self, obj):
        BaseClass.execute(self, obj)
        
        #obj.Impedance = self.model.impedance
        #obj.Resistance  = self.model.resistance
        #obj.Mobility = self.model.mobility
        
        #print self.model.modal_density
        #obj.ModalDensity = map(float, list(self.model.modal_density))
        
       