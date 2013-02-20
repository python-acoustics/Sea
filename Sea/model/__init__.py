"""
The model contains classes describing the physics of all the SEA objects.
Each sort of component, subsystem, coupling, excitation and material has a class of its own.
Every type has a baseclass describing properties that are common.
Ultimately, every object in this module except for System is derived from BaseClass.
System is a class containing methods for solving the SEA model.


"""

from system import *
from components import *
from subsystems import *
from couplings import *
from excitations import *
from materials import *