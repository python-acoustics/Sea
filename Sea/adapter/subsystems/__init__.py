"""
Subsystems module

"""

from longitudinal import SubsystemLong
from bending import SubsystemBend
from shear import SubsystemShear



import inspect, sys
subsystems_map = {item[0]: item[1] for item in inspect.getmembers(sys.modules[__name__], inspect.isclass)}
"""
Dictionary with all available types of subsystems.
"""