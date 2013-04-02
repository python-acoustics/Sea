import Sea
from .. import baseclasses

class ExcitationRain(baseclasses.Excitation):
    """
    Rain on the roof excitation
    """

    name = 'Rain'
    description = 'An excitation averaged over space and time.'
    
    def __init__(self, obj, system, subsystem):
        model = Sea.model.excitations.ExcitationRain
        baseclasses.Excitation.__init__(self, obj, system, subsystem, model)
