import Sea
from .. import baseclasses

class ExcitationPoint(baseclasses.Excitation):
    """
    Rain on the roof excitation
    """

    name = 'Point'
    description = 'An excitation of a single point.'
    
    def __init__(self, obj, system, subsystem):
        model = Sea.model.excitations.ExcitationPoint
        baseclasses.Excitation.__init__(self, obj, system, subsystem, model)
        
        
