""""
The following are Coupling classes encapsulating their respective :mod:`Sea.model.couplings` class.
"""


import logging

import Sea
import baseclasses

class CouplingJunction(baseclasses.Coupling):
    """
    A coupling describing a connection of a single point.
    """
    name = 'Junction'
    description = 'A coupling describing a connection of a single point.'
    
    model = Sea.model.CouplingJunction()
 
    def __init__(self, obj, system, subsystem_from, subsystem_to, **properties):
        baseclasses.Coupling.__init__(self, obj, system, subsystem_from, subsystem_to, **properties)
        
class CouplingLine(baseclasses.Coupling):
    """
    A coupling describing a connection along a line.
    """
    name = 'Line'
    description = 'A coupling describing a connection along a line.'

    model = Sea.model.CouplingLine()

    def __init__(self, obj, system, subsystem_from, subsystem_to, **properties):
        baseclasses.Coupling.__init__(self, obj, system, subsystem_from, subsystem_to, **properties)
        
class CouplingLine(baseclasses.Coupling):
    """
    A coupling describing a connection along a surface.
    """
    name = 'Surface'
    description = 'A coupling describing a connection along a surface.'
    
    model = Sea.model.CouplingLine()

    def __init__(self, obj, system, subsystem_from, subsystem_to, **properties):
        baseclasses.Coupling.__init__(self, obj, system, subsystem_from, subsystem_to, **properties)
        
        
        

import inspect, sys
couplings_map = {item[0]: item[1] for item in inspect.getmembers(sys.modules[__name__], inspect.isclass)}
"""
Dictionary with all available couplings.
"""