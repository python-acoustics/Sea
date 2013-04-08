import Sea
from Excitation import Excitation

class ExcitationRain(Excitation, Sea.model.excitations.ExcitationRain):
    """
    Rain on the roof excitation
    """

    name = 'Rain'
    description = 'An excitation averaged over space and time.'
    
    
    def __init__(self, obj, subsystem):
        Excitation.__init__(self, obj, subsystem)
