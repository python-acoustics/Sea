from .. import baseclasses

class SubsystemLong(baseclasses.Subsystem):
    """
    Adapter class for longitudinal wave subsystems.
    """
    def __init__(self, obj, component, model):
        baseclasses.Subsystem.__init__(self, obj, component, model)
        component.Proxy.model.subsystem_bend = obj.Proxy.model
        
        
    
    def execute(self, obj):
        baseclasses.Subsystem.execute(self, obj)
        