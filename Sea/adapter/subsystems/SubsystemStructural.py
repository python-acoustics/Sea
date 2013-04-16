import abc


class SubsystemStructural(object):
    """Adapter class for structural components.
    """
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, obj):
        
        obj.addProperty("App::PropertyFloatList", "Velocity", "Subsystem", "Mean velocity.")
        obj.setEditorMode("Velocity", 1)
        obj.addProperty("App::PropertyFloatList", "VelocityLevel", "Subsystem", "Velocity level.")
        obj.setEditorMode("VelocityLevel", 1)
    
    
    def onChanged(self, obj, prop):
        pass
    
    def execute(self, obj):
        
        obj.Velocity = obj.Proxy.velocity.tolist()
        obj.VelocityLevel = obj.Proxy.velocity_level.tolist()
    