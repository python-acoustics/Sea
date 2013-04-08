import abc
import logging
import Sea
import numpy as np
from ..base import Base

class Subsystem(Base):
    """
    Abstract base class for all :mod:`Sea.adapter.subsystems` classes.
    """
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, obj, component):
        """
        Constructor
        
        :param obj: FreeCAD Python Feature object
        :param component: an instance of a child of :class:`Sea.adapter.baseclasses.Component`
        """
        Base.__init__(self, obj)
        
        obj.addProperty("App::PropertyLink", "Component", "Subsystem", "Component this subsystem belongs to.")
        obj.Component = component
        
        obj.addProperty("App::PropertyFloatList", "ModalEnergy", "Subsystem", "Modal energy.")
        obj.Frequency = component.Frequency
        
        obj.addProperty("App::PropertyFloatList", "Impedance", "Subsystem", "Impedance.")
        obj.addProperty("App::PropertyFloatList", "Resistance", "Subsystem", "Resistance.")
        obj.addProperty("App::PropertyFloatList", "Mobility", "Subsystem", "Mobility.")
        obj.addProperty("App::PropertyFloatList", "ModalDensity", "Subsystem", "Modal density.")
        
        obj.addProperty("App::PropertyFloatList", "SoundspeedGroup", "Subsystem", "Group speed.")
        obj.addProperty("App::PropertyFloatList", "SoundspeedPhase", "Subsystem", "Phase speed.")
        obj.addProperty("App::PropertyFloatList", "AverageFrequencySpacing", "Subsystem", "Average frequency spacing.")
        obj.addProperty("App::PropertyFloatList", "Energy", "Subsystem", "Energy.")
        obj.addProperty("App::PropertyFloatList", "Velocity", "Subsystem", "Mean velocity.")
        obj.addProperty("App::PropertyFloatList", "VelocityLevel", "Subsystem", "Velocity level.")
        
        #obj.addProperty("App::PropertyLinkList", "CouplingsFrom", "Couplings", "Couplings that originate from this subsystem.")
        #obj.addProperty("App::PropertyLinkList", "CouplingsTo", "Couplings", "Couplings that end at this subsystem.")
        
        #obj.addProperty("App::PropertyLinkList", "Excitations", "Excitation", "Excitations the subsystem experiences.")
        
        obj.makeExcitation = self.makeExcitation
        
        obj.excitations = self.excitations
        obj.couplingsFrom = self.couplingsFrom
        obj.couplingsTo = self.couplingsTo
        
    def onChanged(self, obj, prop):
        Base.onChanged(self, obj, prop)
        
        if prop == 'Frequency':
            obj.ModalEnergy = np.zeros(obj.Frequency.Amount).tolist()
            
        if prop == 'Component':
            obj.Proxy.component = obj.Component.Proxy
        
        if prop == 'ModalEnergy':
            obj.Proxy.modal_energy = np.array(obj.ModalEnergy)
        
    def execute(self, obj):
        Base.execute(self, obj)
        
        #obj.Impedance = obj.Proxy.impedance.tolist()
        #obj.Resistance  = obj.Proxy.resistance.tolist()
        #obj.Mobility = obj.Proxy.mobility.tolist()
        
        if obj.Component.System.Solved:
            obj.ModalEnergy = obj.Proxy.modal_energy.tolist()
        else:
            obj.ModalEnergy = np.zeros(obj.Frequency.Amount).tolist()
        
        obj.ModalDensity = obj.Proxy.modal_density.tolist()
        
        obj.SoundspeedGroup = obj.Proxy.soundspeed_group.tolist()
        obj.SoundspeedPhase = obj.Proxy.soundspeed_phase.tolist()
        obj.AverageFrequencySpacing = obj.Proxy.average_frequency_spacing.tolist()
        obj.Energy = obj.Proxy.energy.tolist()
        obj.Velocity = obj.Proxy.velocity.tolist()
        obj.VelocityLevel = obj.Proxy.velocity_level.tolist()
    
    @staticmethod
    def excitations(obj):
        """
        Return a list of excitations.
        """
        return filter(Sea.actions.document.isExcitation, obj.InList)
    
    @staticmethod
    def couplingsFrom(obj):
        """
        Return a list of couplings from
        """
        couplings = list()
        for item in obj.InList:
            if Sea.actions.document.isCoupling(item):
                if item.SubsystemFrom.Name == obj.Name:
                    couplings.append(item)
        return couplings
        
    @staticmethod
    def couplingsTo(obj):
        """
        Return a list of couplings from
        """
        couplings = list()
        for item in obj.InList:
            if Sea.actions.document.isCoupling(item):
                if item.SubsystemTo.Name == obj.Name:
                    couplings.append(item)
        return couplings
        
        
    
    @staticmethod
    def makeExcitation(subsystem, sort):
        """
        Add an excitation from :mod:`Sea.adapter.excitations` to the subsystem of component.
        
        :param subsystem: Subsystem that is excited
        :param sort: Type of excitation specified in :class:`Sea.adapter.excitations.excitations_map`
        
        """
        from Sea.adapter.object_maps import excitations_map
        
        obj = subsystem.Document.addObject("App::FeaturePython", 'Excitation')
        excitations_map[sort](obj, subsystem)
        try:
            Sea.adapter.excitations.ViewProviderExcitation(obj.ViewObject)
        except AttributeError:
            pass
        logging.info("Sea: Created %s.", obj.Name)
        obj.Document.recompute()
        return obj    
       
       