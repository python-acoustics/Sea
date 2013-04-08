import abc
import logging

        
class Base(object):
    """Abstract base class for all SEA adapters."""
    __metaclass__ = abc.ABCMeta
    
    name = None
    """
    Human-readable name of the object.
    """
    
    description = None
    """
    Description of the object.
    """
    model = None
    """
    Physics :mod:`Sea.model` object of the respective class.
    """
    
    def __init__(self, obj):
        """
        Constructor
        
        :param obj: FreeCAD Python Feature object
        :param system: :class:`Sea.adapter.system.System` instance
        """
        #system.Objects = system.Objects + [obj]
        
        obj.touch()
        obj.Proxy = self
        self.obj = self
        
        obj.addProperty("App::PropertyString", "ClassName", "SEA", "Name of the class of this object.")
        obj.addProperty("App::PropertyString", "SeaObject", "SEA", "Type of SEA object.")
        obj.addProperty("App::PropertyLink", "Frequency", "SEA", "Link to current frequency settings.")
        
        obj.SeaObject = obj.Proxy.object_sort      
        obj.ClassName = self.__class__.__name__
        
        obj.Label = obj.ClassName
        
        obj.delete = self.delete
        
    def __del__(self):
        logging.info("Object - Destructor - Deleting this object")     
        
        
    def onChanged(self, obj, prop):
        """
        Respond on a change in object :attr:`obj` to property :attr:`prop`.
        
        :param obj: Feature object
        :param prop: Property that was updated
        """
        logging.info("Object %s - onChanged - Changing property %s.", obj.Name, prop)
        
        if prop == 'Frequency':
            obj.Proxy.frequency = obj.Frequency.Proxy
        
        # The object needs to be touched and recomputed so it is guaranteed that all variables are updated accordingly.
        #obj.touch()
        #obj.Document.recompute()
        
    def execute(self, obj):
        """
        This method will be executed on a recomputation.
        
        :param obj: Feature object
        """
        pass
        
        

    @staticmethod
    def delete(obj):
        """
        Remove object from the document.
        """
        import FreeCAD as App
        App.ActiveDocument.removeObject(obj.Name)
        
    #@staticmethod
    #def toList(x):
        #"""
        #Convert :attr:`x` to a list of floats.
        #"""
        #return x.tolist()   # remove this static method, and use x.tolist() directly
    
