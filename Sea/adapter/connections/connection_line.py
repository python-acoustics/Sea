
import Sea
from .. import baseclasses

      
class ConnectionLine(baseclasses.Connection):
    """
    Class for line connections.
    """
    
    def __init__(self, obj, system, components):
        baseclasses.Connection.__init__(self, obj, system, components)
        
    
    def updateComponents(self, obj):
        
        connections = Sea.actions.connection.ShapeConnection([item.Shape for item in obj.Components])
        commons = connections.commons()
        
        if any([item.Edges for item in commons]):
            """
            There is indeed a line connection.
            """
            self.model.components = obj.Components
            self.updateCouplings(obj)
    
