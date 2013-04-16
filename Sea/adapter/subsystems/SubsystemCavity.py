import abc

class SubsystemCavity(object):
    """Adapter class for cavities.
    """
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, obj):
        obj.addProperty("App::PropertyFloatList", "Pressure", "Subsystem", "Mean pressure.")
        obj.setEditorMode("Pressure", 1)
        obj.addProperty("App::PropertyFloatList", "PressureLevel", "Subsystem", "Pressure level.")
        obj.setEditorMode("PressureLevel", 1)
    
    def onChanged(self, obj, prop):
        pass
    
    def execute(self, obj):
        obj.Pressure = obj.Proxy.velocity.tolist()
        obj.PressureLevel = obj.Proxy.velocity_level.tolist()
    