import Sea
from .. import baseclasses

class SubsystemBend(baseclasses.Subsystem):
    """
    Adapter class for bending wave subsystems.
    """
    def __init__(self, obj, component):
        baseclasses.Subsystem.__init__(self, obj, component)
        component.Proxy.model.subsystem_bend = obj.Proxy.model
        
        #obj.addProperty("App::PropertyFloat", "CriticalFrequency", "Bending", "Critical frequency.")
        
    def execute(self, obj):
        baseclasses.Subsystem.execute(self, obj)
        
        
    