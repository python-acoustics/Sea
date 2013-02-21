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
    
    model = Sea.model.System()
    
    def __init__(self, obj):
        """
        :param obj: FeaturePython object 
        """

        #self.model = model.System()
        
        obj.addProperty("App::PropertyLinkList","Objects","System", "Objects linked to SEA System")
        #obj.addProperty("App::PropertyLinkList","Parts","SeaSystem", "Parts linked to SEA System")
        obj.addProperty("App::PropertyLinkList","Components","System", "Components linked to SEA System")
        obj.addProperty("App::PropertyLinkList","Subsystems","SeaSystem", "Subsystems linked to SEA System")
        obj.addProperty("App::PropertyLinkList","Couplings","SeaSystem", "Couplings linked to SEA System")
        obj.addProperty("App::PropertyLinkList","Excitations","SeaSystem", "Couplings linked to SEA System")
        obj.addProperty("App::PropertyLinkList","Materials","SeaSystem", "Materials linked to SEA System")
        
        
        obj.addProperty("App::PropertyBool","IsSeaSystem","System", "True if it is a valid SEA system")
        
        obj.addProperty("App::PropertyFloatList", "Frequency", "System","List of available frequency bands")
        
        obj.addProperty("App::PropertyIntegerList", "EnabledBands", "System","List of enabled frequency bands")
        
        obj.addProperty("App::PropertyBool", "Octaves", "System", "Use 1/1-octaves (True) or 1/3-octaves (False).")        
        obj.addProperty("App::PropertyBool", "Solved", "System", "Boolean showing whether results are present")
        
        obj.Proxy = self
               
        obj.IsSeaSystem=True
        
        self.execute(obj)

        
        
        
    def onChanged(self, obj, prop):
        """
        Do something when a property has changed.
        
        :param obj: FeaturePython object
        :param prop: Name of property that has changed
        """
        if prop == 'Octaves':
            self.model.octaves = obj.Octaves
            
            self.model.enabled_bands = map(bool, np.array(obj.EnabledBands))
            obj.EnabledBands = map(int, list(self.model.enabled_bands))

        elif prop == 'EnabledBands':
            self.model.enabled_bands = map(bool, np.array(obj.EnabledBands))
    
    
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
        
        self.update_objects_lists(obj)

        
    
    def update_objects_lists(self, obj):
        """
        Update the objects lists of the SEA model.
        """
        
        objects = list()
        components = list()
        subsystems = list()
        couplings = list()
        excitations = list()
        materials = list()
        #parts = list()
        
        for item in obj.InList:
            if hasattr(item, 'IsSeaComponent'):
                if item.IsSeaComponent == True:
                    objects.append(item.Proxy.model)
                    components.append(item.Proxy.model)
            elif hasattr(item, 'IsSeaSubsystem'):
                if item.IsSeaSubsystem == True:
                    objects.append(item.Proxy.model)
                    subsystems.append(item.Proxy.model)
            elif hasattr(item, 'IsSeaCoupling'):
                if item.IsSeaCoupling == True:
                    objects.append(item.Proxy.model)
                    couplings.append(item.Proxy.model)
            elif hasattr(item, 'IsSeaExcitation'):
                if item.IsSeaExcitation == True:
                    objects.append(item.Proxy.model)
                    excitations.append(item.Proxy.model)
            elif hasattr(item, 'IsSeaMaterial'):
                if item.IsSeaMaterial == True:
                    objects.append(item.Proxy.model)
                    couplings.append(item.Proxy.model)
                    
        self.model.objects = objects
        self.model.components = components
        self.model.subsystems = subsystems
        self.model.couplings = couplings
        self.model.excitations = excitations
        self.model.materials = materials

