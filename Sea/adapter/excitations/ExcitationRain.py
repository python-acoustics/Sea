import Sea
from .. import baseclasses

class ExcitationRain(baseclasses.Excitation):
    """
    Rain on the roof excitation
    """

    name = 'Rain'
    description = 'An excitation averaged over space and time.'
    
    model = Sea.model.excitations.ExcitationRain()
    
    def __init__(self, obj, subsystem):
        baseclasses.Excitation.__init__(self, obj, subsystem)
