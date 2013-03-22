

import Sea
from .. import baseclasses

class ConnectionPoint(baseclasses.Connection):
    
    def __init__(self, obj, system, components):
        baseclasses.Connection.__init__(self, obj, system, components)
       
        #obj.Sort = 'Point'
        
    def updateComponents(self, obj):
        
        connections = Sea.actions.connection.ShapeConnection([item.Shape for item in obj.Components])
        commons = connections.commons()
        
        if any([item.Vertexes for item in commons]):
            """
            There is indeed a point connection.
            """
            self.model.components = obj.Components
            self.updateCouplings(obj)
    