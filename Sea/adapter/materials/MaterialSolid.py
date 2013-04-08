import Sea
from Material import Material

class MaterialSolid(Material, Sea.model.materials.MaterialSolid):
    """
    Solid material
    """
    name = 'Solid'
    description = 'A material in solid state.'
    
    def __init__(self, obj, system):
        Material.__init__(self, obj, system)

        obj.addProperty("App::PropertyFloat", "Young", "Solid", "Young's modulus").Young=0.0
        obj.addProperty("App::PropertyFloat", "Shear", "Solid", "Shear modulus").Shear=0.0
        obj.addProperty("App::PropertyFloat", "Poisson", "Solid", "Poisson's ratio").Poisson=0.0
    
    
    def onChanged(self, obj, prop):
        Material.onChanged(self, obj, prop)
        
        if prop == 'Young':
            obj.Proxy.young = obj.Young
        elif prop == 'Shear':
            obj.Proxy.shear = obj.Shear
        elif prop == 'Poisson':
            obj.Proxy.poisson = obj.Poisson
            
    def execute(self, obj):
        Material.execute(self, obj)
 

####class MaterialSolid(Material):
    ####"""
    ####Solid material class
    ####"""

    ##### Elastic moduli
    ####_young = None
    ####_bulk = None
    ####_shear = None
    ####_poisson = None
    ####_isotropic = True     # Whether the material is isotropic or not.    

    #####_tensile_strength_break = None
    #####_tensile_strength_yield = None
    #####_tensile_strength_ultimate = None
    
    #####_tensile_elongation_break = None
    #####_tensile_elongation_yield = None
    #####_tensile_elongation_ultimate = None

    ####def _get_isotropic(self):
        ####"""
        ####Return whether the solid is isotropic or not.
        ####"""        
        #####if self._isotropic is not None:
        ####return self._isotropic
    
    ####def _set_isotropic(self, x):
        ####"""
        ####Set whether the solid is isotropic or not.
        
        ####:param x: is a boolean
        ####"""
        ####if type(x) is bool:   # Perhaps use a try here?
            ####self._isotropic = x

    ####isotropic = property(fget=_get_isotropic, fset=_set_isotropic)
    ####"""
    ####Isotropic material or not.
    ####"""
    
    ####def elastic_moduli_given(self):
        ####"""
        ####Returns the amount of elastic module that were specified.
        ####"""
        ####return (bool(self._young) + bool(self._bulk) + bool(self._shear) + bool(self._poisson))

    
    ####def _del_elastic_moduli(attr):
        ####def del_attr(self):
            ####setattr(self, attr, None)    # Check first whether it can actually be deleted? E.g. when it has not been set at all.
        ####return del_attr
    

    ####def _set_elastic_moduli(attr):
        ####def set_attr(self, x):
            ####if self.elastic_moduli_given() < 2: #and isinstance(x, float):
                ####setattr(self, attr, x)            
            ####else:
                ####warnings.warn('Two elastic moduli have already been set. Please delete one before adding a new one.')
        ####return set_attr
        
  
    ####def _get_elastic_moduli(attr):
        ####"""Retrieve the value of the elastic modulus. Check first whether the value is stored. If not, calculate it from two given moduli."""
        ####def get_attr(self):
            ####if getattr(self, attr) is not None:
                ####return getattr(self, attr) # then we should return it instead of trying to calculate it.
            
            ####elif self.isotropic and self.elastic_moduli_given() >= 2:          # But only when isotropic!!!
                ##### Calculate Bulk
                ####if bool(attr =='_bulk' and self._young and self._shear):
                    ####return (self.young * self.shear) / (9.0 * self.shear - 3.0 * self.young)
                ####elif bool(attr =='_bulk' and self._young and self._poisson):
                    ####return (self.young) / (3.0 - 6.0 * self.poisson)
                ####elif bool(attr =='_bulk' and self._shear and self._poisson):
                    ####return 2.0 * self.shear * (1.0 + self.poisson) / (3.0 - 6.0 * self.poisson)
                ##### Calculate Young
                ####elif bool(attr =='_young' and self._bulk and self._shear):
                    ####return 9.0 * self.bulk * self.shear / (3.0 * self.bulk + self.shear)
                ####elif bool(attr =='_young' and self._bulk and self._poisson):
                    ####return 3.0 * self.bulk * (1.0 - 2.0 * self.poisson)
                ####elif bool(attr =='_young' and self._shear and self._poisson):
                    ####return 2.0 * self.shear * (1.0 + self.poisson)                
                ##### Calculate Shear
                ####elif bool(attr =='_shear' and self._bulk and self._young):
                    ####return 3.0 * self.bulk * self.young / (9 * self.bulk - self.young)
                ####elif bool(attr =='_shear' and self._bulk and self._poisson):
                    ####return 3.0 * self.bulk * (1.0 - 2.0 * self.poisson) / (2.0 + 2.0 * self.poisson)
                ####elif bool(attr =='_shear' and self._young and self._poisson):
                    ####return self.young / (2.0 + 2.0 * self.poisson)
                ##### Calculate Poisson
                ####elif bool(attr =='_poisson' and self._bulk and self._young):
                    ####return ( 3.0 * self.bulk - self.young) / (6.0 * self.bulk)                 
                ####elif bool(attr =='_poisson' and self._bulk and self._shear):
                    ####return (3.0 * self.bulk - 2.0 * self.shear) / (6.0 * self.bulk + 2.0 * self.shear)
                ####elif bool(attr =='_poisson' and self._young and self._shear):
                    ####return (self.young) / (2.0*self.shear) - 1.0
                ####else:
                    ####ValueError
            ####else:
                ####warnings.warn('The modulus was not given for this material and could not be calculated either.')
                    
        ####return get_attr

    ####young = property(fget=_get_elastic_moduli('_young'), fset=_set_elastic_moduli('_young'), fdel=_del_elastic_moduli('_young'))         # Young's modulus, or Tensile modulus
    ####"""
    ####Young's modulus :math:`E`. 
    ####The value can be set or calculated when the material is isotropic and elastic_moduli_given equals two.
    ####"""
    
    ####bulk = property(fget=_get_elastic_moduli('_bulk'), fset=_set_elastic_moduli('_bulk'), fdel=_del_elastic_moduli('_bulk'))            # Bulk modulus
    ####"""
    ####Bulk modulus :math:`K`
    ####The value can be set or calculated when the material is isotropic and elastic_moduli_given equals two.
    ####"""
    
    ####shear = property(fget=_get_elastic_moduli('_shear'), fset=_set_elastic_moduli('_shear'), fdel=_del_elastic_moduli('_shear'))         # Shear modulus
    ####"""
    ####Shear modulus :math:`G`
    ####The value can be set or calculated when the material is isotropic and elastic_moduli_given equals two.
    ####"""
    
    ####poisson = property(fget=_get_elastic_moduli('_poisson'), fset=_set_elastic_moduli('_poisson'), fdel=_del_elastic_moduli('_poisson'))   # Poisson modulus
    ####"""
    ####Poisson ratio :math:`\\nu`
    ####The value can be set or calculated when the material is isotropic and elastic_moduli_given equals two.
    ####"""
        