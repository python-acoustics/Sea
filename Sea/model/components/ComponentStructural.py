
import numpy as np
from Component import Component

class ComponentStructural(Component):
    """
    Abstract base class for structural components.
    """
    availableSubsystems = ['Long', 'Bend', 'Shear']
    