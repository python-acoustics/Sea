
import Sea
import numpy as np

class Frequency(Sea.model.system.Frequency):
    """Adapter class for frequency band settings."""
    
    def __init__(self, obj):
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
            obj.Proxy.center = np.array(obj.Center)
            obj.Enabled = map(int, np.ones(obj.Proxy.amount).tolist())            
        elif prop == 'Upper':
            obj.Proxy.upper = np.array(obj.Upper)
        elif prop == 'Lower':
            obj.Proxy.lower = np.array(obj.Lower)
        elif prop == 'Enabled':
            obj.Proxy.enabled = np.array(obj.Enabled)
        
        
    def execute(self, obj):
        
        obj.Center = obj.Proxy.center.tolist()
        obj.Upper = obj.Proxy.upper.tolist()
        obj.Lower = obj.Proxy.lower.tolist()
        obj.Bandwidth = obj.Proxy.bandwidth.tolist()
        obj.Enabled = obj.Proxy.enabled.tolist()
        obj.Angular = obj.Proxy.angular.tolist()
        obj.Amount = obj.Proxy.amount