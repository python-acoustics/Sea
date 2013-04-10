
import Sea
from Connection import Connection

      
class ConnectionLine(Connection):
    """
    Class for line connections.
    """
    
    def __init__(self, obj, system, components):
        Connection.__init__(self, obj, system, components)
        
    
    def updateComponents(self, obj):
        
        connections = Sea.actions.connection.ShapeConnection([item.Shape for item in obj.Components])
        commons = connections.commons()
        
        if any([item.Edges for item in commons]):
            """
            There is indeed a line connection.
            """
            obj.Proxy.model.components = obj.Components
            obj.updateCouplings()
    
