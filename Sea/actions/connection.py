"""
Actions related to :class:`Sea.adapter.baseclasses.Connection`.
"""

import FreeCAD as App

import Sea
import itertools
import logging


class ShapeConnection(object):
    """
    Class for determining properties of (possibly) connected shapes.
    """
    
    def __init__(self, a, b=None):
        """
        Initialization
        
        :param a: an instance or list of :class:`FreeCAD.TopoShape`
        :param b: an optional instance or list of :class:`FreeCAD.TopoShape`
        
        """
        self.a = a if isinstance(a, list) else [a]
        """
        List of :class:`FreeCAD.TopoShape`
        """
        self.b = b if isinstance(b, list) or b is None else [b]
        """
        List of :class:`FreeCAD.TopoShape`
        """
        
    @staticmethod           
    def _commons_list(x):
        """
        Returns the shapes all objects in x have in common.
        
        :param x: a list of shapes
        
        """
        common = list()
        
        for a, b in itertools.combinations(x, 2):
            c = ShapeConnection._commons_ab(a, b)   # This is what a single combination of shapes have in common.
            for shape in c:     # If any of the shapes in c
                if ShapeConnection._all_connected_ab(x, shape):   # is connected to all the shapes in x.
                    common.append(shape)
        return common
        """For every shape in x, return which they have in common with the list of possible commons."""
        
    @staticmethod
    def _commons_ab(a, b):    
        """
        Returns a list of common shapes between shapes :attr:`a` and :attr:`b`
        
        :param a: an instance of :class:`FreeCAD.TopoShape`
        :param b: an instance of :class:`FreeCAD.TopoShape`
        
        """
        
        com = list()   
                     
        """
        Common volume
        """
        ###for solid_a in a.Solids:
            ###for solid_b in b.Solids:
                ###solid_c = solid_a.common(solid_b)
                ####print solid_c.Volume
                ###com.extend(solid_c.Solids)
        
        """
        Common shell
        """
        for shell_a, shell_b in itertools.product(a.Shells, b.Shells):
            shell_c = shell_a.common(shell_b)
            com.extend(shell_c.Shells)
            com.extend(shell_c.Faces)
            com.extend(shell_c.Edges)
            com.extend(shell_c.Vertexes)
            
        #for face_a, face_b in itertools.product(a.Faces, b.Faces):
            #face_c = face_a.common(face_b)
            #com.extend(face_c.Faces)
            #com.extend(face_c.Edges)
            #com.extend(face_c.Vertexes)
            #com.extend(face_c.Wires)
                
        #for edge_a, edge_b in itertools.product(a.Edges, b.Edges):
            #edge_c = edge_a.common(edge_b)
            #com.extend(edge_c.Faces)
            #com.extend(edge_c.Edges)
            #com.extend(edge_c.Vertexes)
            #com.extend(edge_c.Wires)
        
        return com
    
    
    @staticmethod
    def _all_connected_ab(a, b=None):
        """
        Return True or False depending on whether all of the shapes are connected to eachother.
        
        :param a: an instance or list of :class:`FreeCAD.TopoShape`
        :param b: an instance or list of :class:`FreeCAD.TopoShape`
        
        This function can do two different things:
        * By only giving :attr:`a` it detects whether all of the shapes in the list are connected to eachother.
        * When the optional :attr:`b` is given as well, it detects instead whether all of the shapes in :attr:`a` are connected to all of the shapes in :attr:`b`.
        
        """
        a = a if isinstance(a, list) else [a]
        b = b if isinstance(b, list) or b is None else [b]
        
        if b:
            return all(itertools.starmap(ShapeConnection._commons_ab, itertools.product(a, b)))    
        else:
            return all(itertools.starmap(ShapeConnection._commons_ab, itertools.combinations(a, 2)))    
            
    @staticmethod
    def _any_connected_ab(a, b=None):
        """
        Return True or False depending on whether any of the shapes are connected to eachother.
        
        :param a: an instance or list of :class:`FreeCAD.TopoShape`
        :param b: an instance or list of :class:`FreeCAD.TopoShape`
        
        This function can do two different things:
        * By only giving :attr:`a` it detects whether any of the shapes in the list are connected to eachother.
        * When the optional :attr:`b` is given as well, it detects instead whether any of the shapes in :attr:`a` are connected to any of the shapes in :attr:`b`.
        
        """
        a = a if isinstance(a, list) else [a]
        b = b if isinstance(b, list) or b is None else [b]
        
        if b:
            return any(itertools.starmap(ShapeConnection._commons_ab, itertools.product(a, b)))    
        else:
            return any(itertools.starmap(ShapeConnection._commons_ab, itertools.combinations(a, 2)))    
    
    
    def commons(self):
        """
        Return commons.
        """
        #if len(self.a)==1 and len(self.a)==1:
            #return self.common_ab(self.a[0], self.b[0])
        #else:
        
        if not self.b:
            return self._commons_list(self.a)
        elif len(self.a)==1 and len(self.b)==1:
            return self._commons_ab(self.a[0], self.b[0])
        else:
            raise NotImplementedError
        
    def allConnected(self):
        """
        Return True or False depending on whether all of the shapes are connected to eachother.
        
        This function can do two different things:
        * When only :attr:`self.a` is set, it detects whether all of the shapes in :attr:`self.a` are connected to eachother.
        * When the optional :attr:`self.b` is set as well, it detects instead whether all of the shapes in :attr:`self.a` are connected to all of the shapes in :attr:`self.b`.
        
        """
        return self._all_connected_ab(self.a, self.b)
        
    def anyConnected(self):
        """
        Return True or False depending on whether any of the shapes are connected to eachother.
        
        This function can do two different things:
        * When only :attr:`self.a` is set, it detects whether any of the shapes in :attr:`self.a` are connected to eachother.
        * When the optional :attr:`self.b` is set as well, it detects instead whether any of the shapes in :attr:`self.a` are connected to all of the shapes in :attr:`self.b`.
        
        """
        return self._any_connected_ab(self.a, self.b)
        
    def shape(self):
        """
        Returns the governing shape of the connection.
        
        """
        
        common = self.commons()
        
        solid = None
        face = None
        edge = None
        vertex = None
        
        for shape in common:
            sort = shape.ShapeType
            if sort == 'Solid':
                if solid is None or shape.Volume > solid.Volume:
                    solid = shape
            elif sort == 'Face':
                if face is None or shape.Area > face.Area:
                    face = shape
            elif sort == 'Edge':
                if edge is None or shape.Length > edge.Length:
                    edge = shape
            elif sort == 'Vertex':
                vertex = shape
        
        if solid:
            return solid
        elif face:
            return face
        elif edge:
            return edge
        elif vertex:
            return vertex
        else:
            return None
    
    def sort(self):
        """
        Returns the type of the governing type of the connection.
        """
        shape = self.shape()
        
        types = {
            'Face' : 'surface',
            'Edge' : 'line', 
            'Vertex' : 'point',   
            }
        
        try:
            return types[shape.ShapeType]
        except AttributeError:
            return None
    
        
    
    
#def isConnected(a, b):
    #"""
    #Return True or False depending on whether the shapes are connected or not.
    
    #:param a: a :class:`FreeCAD.TopoShape`
    #:param b: a :class:`FreeCAD.TopoShape`
   
    #"""
    #return bool(commons(a, b))
    

#def yieldConnected(shapes):
    #"""
    #Return tuples of shapes that are connected.
    
    #:param shapes: List of :class:`FreeCAD.TopoShape`
    
    #"""
    #return 
    
    #any([bool(commons(a,b)) for a, b in itertools.combinations(shapes, 2))

    
    
def hasShapeType(items, sort):
    """
    Detect whether the list has any items of type sort. Returns :attr:`True` or :attr:`False`.
    :param shape: :class:`list`
    :param sort: type of shape
    """
    return any([getattr(item, sort) for item in items])
                
#def addComponent(connection, component):
    #"""
    #Add component to the connection. Test whether the component really is connected.
        
    #:param connection: an instance of :class:`Sea.adapter.connection.Connection`
    #:param component: an instance of a child of :class:`Sea.adapter.baseclasses.Component`
    #"""
    
    #if connection.Components:
        #"""There are components. Test whether this new one connects to any."""
        #if component not in connection.Components:
            #"""It shouldn't already be in the list of components."""
            
            #if ShapeConnection( [item.Shape for item in connection.Components], component.Shape).anyConnected():
                #"""If there is any connection..."""
                #print 'Thereis a connection\n'
                #connection.Components = connection.Components + [component]
            #else:
                #pass
                #App.Console.PrintWarning("Component was not added to the Connection as there was no connection to any of the other components.\n")
        #else:
            #App.Console.PrintWarning("Component was already added to this connection.\n")
    #else:
        #"""
        #This is the first component added to the connection. Therefore add it straight away.
        #"""
        #connection.Components = connection.Components + [component]
    
    #connection.Document.recompute()
    
            
    