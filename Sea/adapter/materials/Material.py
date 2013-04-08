
import abc
import logging
import Sea
import numpy as np
from ..base import Base



class Material(Base):
    """
    Abstract base class for all :mod:`Sea.adapter.materials` classes.
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, obj, system):
        obj.addProperty("App::PropertyLinkList", "Components", "Material", "Components that make use of this material.")
        Base.__init__(self, obj)
        
        obj.addProperty("App::PropertyLink", "System", "Material", "System this material belongs to.")
        obj.System = system
        
        obj.Frequency = system.Frequency
        
        obj.addProperty("App::PropertyFloat", "Density", "Material", "Density of the material.").Density=0.0
        obj.addProperty("App::PropertyFloatList", "LossFactor", "Material", "Loss factor of the material.").LossFactor=0.0
        obj.addProperty("App::PropertyFloat", "Temperature", "Material", "Temperature of the material.").Temperature=0.0
        obj.addProperty("App::PropertyFloat", "Pressure", "Material", "Pressure of the material.").Pressure=0.0
        obj.addProperty("App::PropertyFloat", "Bulk", "Material", "Bulk modulus of the material").Bulk=0.0
        
        obj.reassignMaterials = self.reassignMaterials
        obj.replaceWith = self.replaceWith
        
    def onChanged(self, obj, prop):
        Base.onChanged(self, obj, prop)
        
        for comp in obj.Components:
            comp.touch()
            for sub in comp.Subsystems:
                sub.touch()
        
        if prop == 'Density':
            obj.Proxy.density = obj.Density
        elif prop == 'LossFactor':
            if len(obj.LossFactor) == 1:
                obj.Proxy.loss_factor = np.ones(obj.Frequency.Amount) * np.array(obj.LossFactor)
            else:
                obj.Proxy.loss_factor = np.array(obj.LossFactor)
        elif prop == 'Temperature':
            obj.Proxy.temperature = obj.Temperature
        elif prop == 'Pressure':
            obj.Proxy.pressure = obj.Pressure
        elif prop == 'Bulk':
            obj.Proxy.bulk = obj.Bulk
        
        
    def execute(self, obj):
        obj.Density = obj.Proxy.density
        obj.LossFactor = obj.Proxy.loss_factor.tolist()
        obj.Temperature = obj.Proxy.temperature
        obj.Pressure = obj.Proxy.pressure
        obj.Bulk = obj.Proxy.bulk
    
    @staticmethod
    def reassignMaterials(material, materials):
        """
        Assign :attr:`material` to all components making use of :attr:`materials`.
        """
        materials = [materials] if not isinstance(materials, list) else materials
        
        for mat in materials:
            mat.replaceWith(material)
        
    @staticmethod
    def replaceWith(material, new_material):
        """
        Replace all objects that use :attr:`material` with :attr:`new_material`.
        """
        for comp in material.Components:
            comp.changeMaterial(new_material)
        