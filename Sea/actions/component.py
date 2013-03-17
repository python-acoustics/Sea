"""
Actions related to children of :class:`Sea.adapter.baseclasses.Component`
"""

import itertools

def determine_structural_sort(part):
    """
    Determine which component describes the :class:`FreeCAD.Shape` best
    
    :param part: :class:`FreeCAD.Part` to be investigated
    """
    
    if part.Type == 'Part::Box':
        box = part.Shape.BoundBox
        
        # Right now a rudimentary guess based on the shape.
        # Correct method would be Lyon, page 138
        
        dim = {'x': box.XLength, 'y': box.YLength, 'z': box.ZLength}
        
        pairs = [(x[0],y[0]) for x, y in itertools.permutations(dim.iteritems(), 2) if x[1] > 2 * y[1] ]
        
        length = len(pairs)
        
        if length == 4:
            return "Component1DBeam"
        elif length == 2:
            return "Component2DPlate"
        elif length == 0:
            return "Component3DBox"
    
def determine_cavity_sort(shape):
    
    return "Component3DCavity"