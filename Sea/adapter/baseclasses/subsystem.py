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
    
    def __init__(self, obj, component):
        """
        Constructor
        
        :param obj: FreeCAD Python Feature object
        :param component: an instance of a child of :class:`Sea.adapter.baseclasses.Component`
        """
        BaseClass.__init__(self, obj)
        obj.Proxy.model.component = component.Proxy.model
        obj.Frequency = component.Frequency
        component.Subsystems = component.Subsystems + [obj]
        obj.addProperty("App::PropertyString", "Component", "Subsystem", "Component this subsystem belongs to.")
        
        obj.Component = component.Name
        obj.addProperty("App::PropertyFloatList", "Impedance", "Subsystem", "Impedance.")
        obj.addProperty("App::PropertyFloatList", "Resistance", "Subsystem", "Resistance.")
        obj.addProperty("App::PropertyFloatList", "Mobility", "Subsystem", "Mobility.")
        obj.addProperty("App::PropertyFloatList", "ModalDensity", "Subsystem", "Modal density.")
        obj.addProperty("App::PropertyFloatList", "ModalEnergy", "Subsystem", "Modal energy.")
        obj.addProperty("App::PropertyFloatList", "SoundspeedGroup", "Subsystem", "Group speed.")
        obj.addProperty("App::PropertyFloatList", "SoundspeedPhase", "Subsystem", "Phase speed.")
        obj.addProperty("App::PropertyFloatList", "AverageFrequencySpacing", "Subsystem", "Average frequency spacing.")
        obj.addProperty("App::PropertyFloatList", "Energy", "Subsystem", "Energy.")
        obj.addProperty("App::PropertyFloatList", "Velocity", "Subsystem", "Mean velocity.")
        obj.addProperty("App::PropertyFloatList", "VelocityLevel", "Subsystem", "Velocity level.")
        
        obj.addProperty("App::PropertyLinkList", "CouplingsFrom", "Couplings", "Couplings that originate from this subsystem.")
        obj.addProperty("App::PropertyLinkList", "CouplingsTo", "Couplings", "Couplings that end at this subsystem.")
        
        obj.addProperty("App::PropertyLinkList", "Excitations", "Excitation", "Excitations the subsystem experiences.")
        obj.Excitations = []
        
        obj.makeExcitation = self.makeExcitation
        
    def onChanged(self, obj, prop):
        BaseClass.onChanged(self, obj, prop)
        
        if prop == 'CouplingsFrom':
            #for coupling in obj.CouplingsFrom:
                #coupling.Proxy.model.subsystem_from = obj.Proxy.model
            obj.Proxy.model.linked_couplings_from = [coupling.Proxy.model for coupling in obj.CouplingsFrom]
        elif prop == 'CouplingsTo':
            #for coupling in obj.CouplingsTo:
                #coupling.Proxy.model.subsystem_to = obj.Proxy.model        
            obj.Proxy.model.linked_couplings_to = [coupling.Proxy.model for coupling in obj.CouplingsTo]
        elif prop == 'Excitations':
            obj.Proxy.model.linked_excitations = [excitation.Proxy.model for excitation in obj.Excitations]
        
        if prop =='Frequency':
            obj.Proxy.model.modal_energy = np.zeros(len(obj.Frequency.Center))
        
    def execute(self, obj):
        BaseClass.execute(self, obj)
        
        #obj.Impedance = obj.Proxy.model.impedance.tolist()
        #obj.Resistance  = obj.Proxy.model.resistance.tolist()
        #obj.Mobility = obj.Proxy.model.mobility.tolist()
        
        
        
        obj.ModalDensity = obj.Proxy.model.modal_density.tolist()
        obj.ModalEnergy = obj.Proxy.model.modal_energy.tolist()
        obj.SoundspeedGroup = obj.Proxy.model.soundspeed_group.tolist()
        obj.SoundspeedPhase = obj.Proxy.model.soundspeed_phase.tolist()
        obj.AverageFrequencySpacing = obj.Proxy.model.average_frequency_spacing.tolist()
        obj.Energy = obj.Proxy.model.energy.tolist()
        obj.Velocity = obj.Proxy.model.velocity.tolist()
        obj.VelocityLevel = obj.Proxy.model.velocity_level.tolist()
        
    @staticmethod
    def makeExcitation(subsystem, sort):
        """
        Add an excitation from :mod:`Sea.adapter.excitations` to the subsystem of component.
        
        :param subsystem: Subsystem that is excited
        :param sort: Type of excitation specified in :class:`Sea.adapter.excitations.excitations_map`
        
        """
        from Sea.adapter.object_maps import excitations_map
        
        obj = subsystem.newObject("App::FeaturePython", 'Excitation')
        excitations_map[sort](obj, subsystem)
        logging.info("Sea: Created %s.", obj.Name)
        obj.Document.recompute()
        return obj    
       
       
       
class SubsystemLong(Subsystem):
    """
    Adapter class for longitudinal wave subsystems.
    """
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, obj, component):
        Subsystem.__init__(self, obj, component)
        component.Proxy.model.subsystem_long = obj.Proxy.model
        
class SubsystemBend(Subsystem):
    """
    Adapter class for bending wave subsystems.
    """
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, obj, component):
        Subsystem.__init__(self, obj, component)
        component.Proxy.model.subsystem_bend = obj.Proxy.model

class SubsystemShear(Subsystem):
    """
    Adapter class for shear wave subsystems.
    """
    def __init__(self, obj, component):
        Subsystem.__init__(self, obj, component)
        component.Proxy.model.subsystem_shear = obj.Proxy.model
        
                   