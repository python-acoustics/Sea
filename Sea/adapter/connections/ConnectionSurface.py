
import Sea
from Connection import Connection


class ConnectionSurface(Connection):
    """
    Class for surface connections.
    """
    
    def __init__(self, obj, system, components):
        Connection.__init__(self, obj, system, components)
        
        #obj.Sort = 'Surface'
        
        
    def updateComponents(self, obj):
        
        connections = Sea.actions.connection.ShapeConnection([item.Shape for item in obj.Components])
        commons = connections.commons()
        
        if any([item.Faces for item in commons]):
            """
            There is indeed a surface connection.
            """
            obj.Proxy.model.components = obj.Components
            obj.updateCouplings()
        

