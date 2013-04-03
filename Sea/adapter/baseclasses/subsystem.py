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
        BaseClass.__init__(self, obj, model)
        obj.Model.component = component.Model
        obj.Frequency = component.Frequency
        component.Subsystems = component.Subsystems + [obj]
        
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
                #coupling.Model.subsystem_from = obj.Model
            obj.Model.linked_couplings_from = [coupling.Model for coupling in obj.CouplingsFrom]
        elif prop == 'CouplingsTo':
            #for coupling in obj.CouplingsTo:
                #coupling.Model.subsystem_to = obj.Model        
            obj.Model.linked_couplings_to = [coupling.Model for coupling in obj.CouplingsTo]
        elif prop == 'Excitations':
            obj.Model.linked_excitations = [excitation.Model for excitation in obj.Excitations]
        
        if prop =='Frequency':
            obj.Model.modal_energy = np.zeros(len(obj.Frequency))
        
    def execute(self, obj):
        BaseClass.execute(self, obj)
        
        #obj.Impedance = obj.Model.impedance.tolist()
        #obj.Resistance  = obj.Model.resistance.tolist()
        #obj.Mobility = obj.Model.mobility.tolist()
        
        
        
        obj.ModalDensity = obj.Model.modal_density.tolist()
        obj.ModalEnergy = obj.Model.modal_energy.tolist()
        obj.SoundspeedGroup = obj.Model.soundspeed_group.tolist()
        obj.SoundspeedPhase = obj.Model.soundspeed_phase.tolist()
        obj.AverageFrequencySpacing = obj.Model.average_frequency_spacing.tolist()
        obj.Energy = obj.Model.energy.tolist()
        obj.Velocity = obj.Model.velocity.tolist()
        obj.VelocityLevel = obj.Model.velocity_level.tolist()
        
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
       