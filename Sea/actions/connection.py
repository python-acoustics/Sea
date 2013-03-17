"""
Actions related to :class:`Sea.adapter.baseclasses.Connection`.
"""

import FreeCAD as App

import Sea
import itertools
import logging

coupling_options = {
        
        ('point', 'Component1DBeam', 'Component1DBeam') : 'Coupling1DStructural',
        ('line', 'Component1DBeam', 'Component1DBeam') : 'Coupling1DStructural',
        ('surface', 'Component1DBeam', 'Component1DBeam') : 'Coupling1DStructural',
        ('point', 'Component2DPlate', 'Component2DPlate') : 'Coupling1DStructural',
        ('line', 'Component2DPlate', 'Component2DPlate') : 'Coupling2DStructural',
        ('surface', 'Component2DPlate', 'Component2DPlate') : 'Coupling2DStructural',
        
        ('surface', 'Component2DPlate', 'Component3DCavity') : 'Coupling3DPlateCavity',
        ('surface', 'Component3DCavity', 'Component2DPlate') : 'Coupling3DCavityPlate',
        }


def commons(a, b):    
    """
    Returns a list of common shapes between shapes :attr:`a` and :attr:`b`
    
    :param a: a :class:`FreeCAD.TopoShape`
    :param b: a :class:`FreeCAD.TopoShape`
    
    """
    commons = list()            
                          
    """
    Common volume
    """
    ###for solid_a in a.Solids:
        ###for solid_b in b.Solids:
            ###solid_c = solid_a.common(solid_b)
            ####print solid_c.Volume
            ###commons.extend(solid_c.Solids)
    
    """
    Common shell
    """
    for shell_a, shell_b in itertools.product(a.Shells, b.Shells):
        shell_c = shell_a.common(shell_b)
        commons.extend(shell_c.Shells)
        commons.extend(shell_c.Faces)
        commons.extend(shell_c.Edges)
        commons.extend(shell_c.Vertexes)
        
    for face_a, face_b in itertools.product(a.Faces, b.Faces):
        face_c = face_a.common(face_b)
        commons.extend(face_c.Faces)
        commons.extend(face_c.Edges)
        commons.extend(face_c.Vertexes)
        commons.extend(face_c.Wires)
            
    for edge_a, edge_b in itertools.product(a.Edges, b.Edges):
        edge_c = edge_a.common(edge_b)
        commons.extend(edge_c.Faces)
        commons.extend(edge_c.Edges)
        commons.extend(edge_c.Vertexes)
        commons.extend(edge_c.Wires)
    
    return commons
    
    
#def isConnected(a, b):
    #"""
    #Return True or False depending on whether the shapes are connected or not.
    
    #:param a: a :class:`FreeCAD.TopoShape`
    #:param b: a :class:`FreeCAD.TopoShape`
   
    #"""
    #return bool(commons(a, b))
    

def isConnected(shapes, shape=None):
    """
    Return True or False depending on whether all of the shapes are connected to eachother.
    
    :param shapes: List of :class:`FreeCAD.TopoShape`
    :param shape: An instance of :class:`FreeCAD.TopoShape`
    
    This function can do two different things:
    * By only giving :attr:`Shapes` it detects whether all of the shapes are connected to eachother.
    * When the optional :attr:`Shape` is given as well, it detects instead whether all of the :attr:`Shapes` are connected to the :attr:`Shape`
    
    """
    #print shape
    if shape:
        try:
            return all(itertools.starmap(commons, itertools.product(shapes, [shape])))    
        except TypeError:
            return all(itertools.starmap(commons, itertools.product([shapes], [shape])))    
    else:
        return all(itertools.starmap(commons, itertools.combinations(shapes, 2)))    
        
def anyConnected(shapes, shape=None):
    """
    Return True or False depending on whether any of the shapes are connected to eachother.
    
    :param shapes: List of :class:`FreeCAD.TopoShape`
    :param shape: An instance of :class:`FreeCAD.TopoShape`
    
    This function can do two different things:
    * By only giving :attr:`Shapes` it detects whether any of the shapes are connected to eachother.
    * When the optional :attr:`Shape` is given as well, it detects instead whether any of the :attr:`Shapes` are connected to the :attr:`Shape`
    
    """
    if shape:
        try:
            return any([bool(commons(a, shape)) for a in shapes])
        except TypeError:
            shapes = [shapes]
    else:
        try:
            return any(itertools.starmap(commons, itertool.combinations(shapes, 2)))    
        except TypeError:
            shapes = [shapes]
    
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
    

def determineConnectionShape(a, b):
    """
    Returns the governing shape connecting shapes a and b.
    
    :param: a :class:`FreeCAD.TopoShape`
    :param: b :class:`FreeCAD.TopoShape`
    
    """
    common = commons(a, b)
    
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
    
def determineConnectionType(a, b):
    """
    Returns the type of the governing shape of the connection between shapes a and b.
    """
    shape = determineConnectionShape(a, b)
    
    types = {
        'Face' : 'surface',
        'Edge' : 'line', 
        'Vertex' : 'point',   
        }
    
    if shape:
        return types[shape.ShapeType]
    else:
        return None
    
    
#def determineConnectionType(a, b):
    #"""
    #Determine whether shapes a and b are connected through a surface, line or point.
    #"""
    #common = commons(a, b)

    #if hasShapeType(common, 'Solids'):
        
        #for item in common:
            #for solid in item.Solids:
                #print solid.Volume
        #App.Console.PrintWarning("Shapes share a solid!\n")
        #return None
    
    #elif hasShapeType(common, 'Faces'):
        #"""
        #Shape has faces. That means a surface connection.
        #"""
        #return 'surface'
    
    #elif hasShapeType(common, 'Edges'):
        #"""
        #Shape has edges. That means a line connection.
        #"""
        #return 'line'
    
    #elif hasShapeType(common, 'Vertexes'):
        #"""
        #Shape has vertices. That means a point connection.
        #"""
        #return 'point'
            
def determineCouplingType(connection_type, component_from, component_to):
    """
    Determine the type of coupling. Detects what type of connection the components have.
    Based on the type of connection and on the types of components a coupling is returned.
    
    :param component_from: an instance of a child of :class:`Sea.adapter.baseclasses.Component`
    :param component_to: an instance of a child of :class:`Sea.adapter.baseclasses.Component`
    """
    
    if connection_type:
        item = (connection_type, component_from.ClassName, component_to.ClassName)   
        try:
            return coupling_options[item]
        except KeyError:
            txt = 'Could not determine the type of coupling for ' + component_from.ClassName + ' to ' + component_to.ClassName + ' with ' + connection_type +  '.\n'
            App.Console.PrintWarning(txt)
            return None
            
def addComponent(connection, component):
    """
    Add component to the connection. Test whether the component really is connected.
        
    :param connection: an instance of :class:`Sea.adapter.connection.Connection`
    :param component: an instance of a child of :class:`Sea.adapter.baseclasses.Component`
    """
    
    if connection.Components:
        """There are components. Test whether this new one connects to any."""
        if component not in connection.Components:
            """It shouldn't already be in the list of components."""
            if any( [ isConnected(component.Shape, item.Shape) for item in connection.Components ]):
                """If there is any connection..."""
                connection.Components = connection.Components + [component]
            else:
                App.Console.PrintWarning("Component was not added to the Connection as there was no connection to any of the other components.")
        else:
            App.Console.PrintWarning("Component was already added to this connection.\n")
    else:
        """
        This is the first component added to the connection. Therefore add it straight away.
        """
        connection.Components = connection.Components + [component]

            
def addCoupling(system, connection, component_from, subsystems_from, component_to, subsystems_to, reverse, connection_type=None):
    """
    Add a coupling to the :attr:`connection`.
    
    :param connection: an instance of :class:`Sea.adapter.baseclasses.Connection`
    :param component_from: an instance of a child of `Sea.adapter.baseclasses.Component`
    :param subsystems_from: list of strings specifying the type of subsystem.
    :param component_to: an instance of a child of `Sea.adapter.baseclasses.Component`
    :param subsystems_to: list of strings specifying the type of subsystem.
    :param connection_type: type of connection between the components. Default is to determine it automatically.
    :param reverse: a :class:`bool` indicating whether the reverse coupling should be added as well.
    """ 
    
    if not isinstance(subsystems_from, list):
        subsystems_from = [subsystems_from]
    if not isinstance(subsystems_to, list):
        subsystems_from = [subsystems_to]
    
    if not connection_type:
        connection_type = determineConnectionType(component_from.Shape, component_to.Shape)
    
    
    
    coupling_sort = determineCouplingType(connection_type, component_from, component_to)
    
    if coupling_sort is None:
        App.Console.PrintWarning("Cannot add coupling.\n")
        return
    
    for sub_from, sub_to in itertools.product(subsystems_from, subsystems_to):
        Sea.actions.factory.makeCoupling(system, connection, component_from, sub_from, component_to, sub_to, coupling_sort)
    
    if reverse:
        """
        Do the same trick but now for the reverse case.
        """
        addCoupling(system, connection, component_to, subsystems_to, component_from, subsystems_from, False, connection_type)
        
def addCouplings(system, connection):
    """
    Add all possible couplings to :attr:`connection`.
    
    :param connection: an instance of :class:`Sea.adapter.baseclasses.Connection`
    """
    
    for comp_a, comp_b in itertools.combinations(connection.Components, 2):
        Sea.actions.connection.addCoupling(system, connection, comp_a, comp_a.AvailableSubsystems, comp_b, comp_b.AvailableSubsystems, True, connection.Sort)
                
        
    
    
    