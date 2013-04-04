
import Sea
import numpy as np

class Frequency(object):
    """Adapter class for frequency band settings."""
    
    model = Sea.model.baseclasses.Frequency()
    """
    Model
    """
    
    def __init__(self, obj, system):
        obj.Proxy = self
        
        obj.addProperty("App::PropertyFloatList", "Center", "Frequency", "Centerfrequencies of frequency bands.")
        obj.addProperty("App::PropertyFloatList", "Lower", "Frequency", "Lower limit frequencies of frequency bands.")
        obj.addProperty("App::PropertyFloatList", "Upper", "Frequency", "Upper limit frequencies of frequency bands.")
        obj.addProperty("App::PropertyFloatList", "Bandwidth", "Frequency", "Bandwidth of frequency bands.")
        obj.addProperty("App::PropertyFloatList", "Angular", "Frequency", "Angular centerfrequencies of frequency bands.")
        obj.addProperty("App::PropertyIntegerList", "Enabled", "System","List of enabled frequency bands")
        obj.addProperty("App::PropertyInteger", "Amount", "Amount of frequency bands.")
        
        self.execute(obj)
        
    def onChanged(self, obj, prop):
        
        obj.touch()
        
        if prop == 'Center':
            obj.Proxy.model.center = np.array(obj.Center)
            obj.Enabled = map(int, np.ones(obj.Proxy.model.amount).tolist())            
        elif prop == 'Upper':
            obj.Proxy.model.upper = np.array(obj.Upper)
        elif prop == 'Lower':
            obj.Proxy.model.lower = np.array(obj.Lower)
        elif prop == 'Enabled':
            obj.Proxy.model.enabled = np.array(obj.Enabled)
        
        
    def execute(self, obj):
        
        obj.Center = obj.Proxy.model.center.tolist()
        obj.Upper = obj.Proxy.model.upper.tolist()
        obj.Lower = obj.Proxy.model.lower.tolist()
        obj.Bandwidth = obj.Proxy.model.bandwidth.tolist()
        obj.Enabled = obj.Proxy.model.enabled.tolist()
        obj.Angular = obj.Proxy.model.angular.tolist()
        obj.Amount = obj.Proxy.model.amount