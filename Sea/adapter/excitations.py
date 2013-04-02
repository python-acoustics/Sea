"""
The following are Excitation classes encapsulating their respective :mod:`Sea.model.excitations` class.
"""


import logging

import Sea
import baseclasses

class ExcitationPoint(baseclasses.Excitation):
    """
    Rain on the roof excitation
    """

    name = 'Point'
    description = 'An excitation of a single point.'
    
    def __init__(self, obj, system, subsystem):
        model = Sea.model.excitations.ExcitationPoint()
        baseclasses.Excitation.__init__(self, obj, system, subsystem, model)
        
        
        
        
class ExcitationRain(baseclasses.Excitation):
    """
    Rain on the roof excitation
    """

    name = 'Rain'
    description = 'An excitation averaged over space and time.'
    
    def __init__(self, obj, system, subsystem):
        model = Sea.model.excitations.ExcitationRain()
        baseclasses.Excitation.__init__(self, obj, system, subsystem, model)
        
        
    
import inspect, sys
excitations_map = {item[0]: item[1] for item in inspect.getmembers(sys.modules[__name__], inspect.isclass)}
"""
Dictionary with all available excitations.
"""