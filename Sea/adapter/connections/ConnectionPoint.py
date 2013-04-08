
import Sea
from Connection import Connection


class ConnectionPoint(Connection):
    """
    Class for point connections.
    """
    
    def __init__(self, obj, system, components):
        Connection.__init__(self, obj, system, components)
       
        #obj.Sort = 'Point'
        
    def updateComponents(self, obj):
        
        connections = Sea.actions.connection.ShapeConnection([item.Shape for item in obj.Components])
        commons = connections.commons()
        
        if any([item.Vertexes for item in commons]):
            """
            There is indeed a point connection.
            """
            obj.Proxy.model.components = obj.Components
            obj.updateCouplings()
    