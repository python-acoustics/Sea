
import abc
import math
import cmath
import numpy as np

from ..base import Base

class Material(Base):
    """
    Abstract Material Class
    """
    __metaclass__ = abc.ABCMeta
    
    object_sort = 'Material'
    
    linked_components = None
    """
    Components linked to this subsystem.
    """

    density = 0.0
    """
    Density :math:`\\rho` of the material.
    """
    
    loss_factor = np.array([0.0])
    """
    Loss factor :math:`\\eta` of the material.
    """
    
    temperature = 0.0
    """
    Temperature :math:`T`
    """
      
    pressure = 0.0
    """
    Pressure :math:`p`
    """

    bulk = 0.0
    """
    Bulk modulus
    """