
import abc
import logging
import FreeCAD as App

import FreeCAD, FreeCADGui
from pivy import coin

import Sea

import numpy as np


import abc
import logging
import Sea
import numpy as np
from baseclass import BaseClass
        
class Material(BaseClass):
    """
    Abstract base class for all :mod:`Sea.adapter.materials` classes.
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, obj, system, model):
        obj.addProperty("App::PropertyLinkList", "Components", "Material", "Components that make use of this material.")
        BaseClass.__init__(self, obj, model)
        system.Materials = system.Materials + [obj]
        obj.Frequency = system.Frequency
        
        obj.addProperty("App::PropertyFloat", "Density", "Material", "Density of the material.").Density=0.0
        obj.addProperty("App::PropertyFloatList", "LossFactor", "Material", "Loss factor of the material.").LossFactor=0.0
        obj.addProperty("App::PropertyFloat", "Temperature", "Material", "Temperature of the material.").Temperature=0.0
        obj.addProperty("App::PropertyFloat", "Pressure", "Material", "Pressure of the material.").Pressure=0.0
        obj.addProperty("App::PropertyFloat", "Bulk", "Material", "Bulk modulus of the material").Bulk=0.0
        
        obj.reassignMaterials = self.reassignMaterials
        obj.replaceWith = self.replaceWith
        
    def onChanged(self, obj, prop):
        BaseClass.onChanged(self, obj, prop)
        
        for comp in obj.Components:
            comp.touch()
            for sub in comp.Subsystems:
                sub.touch()
        
        if prop == 'Density':
            obj.Model.density = obj.Density
        elif prop == 'LossFactor':
            if len(obj.LossFactor) == 1:
                obj.Model.loss_factor = np.ones(len(obj.Frequency)) * np.array(obj.LossFactor)
            else:
                obj.Model.loss_factor = np.array(obj.LossFactor)
        elif prop == 'Temperature':
            obj.Model.temperature = obj.Temperature
        elif prop == 'Pressure':
            obj.Model.pressure = obj.Pressure
        elif prop == 'Bulk':
            obj.Model.bulk = obj.Bulk
        
        
    def execute(self, obj):
        obj.Density = obj.Model.density
        obj.LossFactor = obj.Model.loss_factor.tolist()
        obj.Temperature = obj.Model.temperature
        obj.Pressure = obj.Model.pressure
        obj.Bulk = obj.Model.bulk
    
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
        