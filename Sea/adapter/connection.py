"""
Module containing Connection class.
"""

import Sea

import baseclasses

class Connection(baseclasses.BaseClass):
    """
    Adapter class for :class:`Sea.model.connection.Connection`.
    """
    
    model = Sea.model.connection.Connection
    
    def __init__(self, obj, system, sort):
        baseclasses.BaseClass.__init__(self, obj, system, 'Connection')
        
        obj.addProperty("App::PropertyLinkList", "Components", "Connection", "Components that are connected via this coupling.")
        
        #obj.addProperty("App::PropertyList", "Subsystems", "Connection", "Components that are connected via this coupling.")
        """
        List of tuples?
        """
        
        #obj.addProperty("App::PropertyList", "Couplings", "Coupling", "List of all couplings.")

        #obj.addProperty("App::PropertyList", "PossibleRoutes", "Coupling", "All possible combinations of couplings.")
        
        obj.addProperty("App::PropertyString", "Sort", "Connection", "Is the connection described by a point, line or area.")
        
        obj.Sort = sort
        
    def onChanged(self, obj, prop):
        baseclasses.BaseClass.onChanged(self, obj, prop)
        
        ##if prop == 'Components':
            ##"""
            ##Update lists of components as well as list of enabled subsystems.
            ##"""
            
            ##components = list()
            ##subsystems = list()
            ##for component in obj.Components:
                ##self.model.components.append(component.Proxy.model)
                ##if hasattr(component, 'EnableLong'):
                    ##if obj.EnableLong == True:
                        ##subsystems.append(component.Proxy.model.subsystem_long)
                ##if hasattr(component, 'EnableLong'):
                    ##if obj.EnableLong == True:
                        ##subsystems.append(component.Proxy.model.subsystem_bend)
                ##if hasattr(component, 'EnableLong'):
                    ##if obj.EnableLong == True:
                        ##subsystems.append(component.Proxy.model.subsystem_shear) 
            ##self.model.components = components
            ##self.model.subsystems = subsystems
            
            ##obj.Subsystems = subsystems

            ###routes = list()
            ###for subsystem_a in subsystems:
                ###for subsystem_b in subsystems:
                    ###if subsystem_a.component != subsystem_b.component:
                        ###routes.append((subsystem_a, subsystem_b))                        
            ###obj.PossibleRoutes = routes
            ###obj.Routes = self.model.routes
            
            ##couplings = list()
            ##couplings_tuples = list()
            ##for subsystem_a in subsystems:
                ##for subsystem_b in subsystems:
                    ##if subsystem_a.component != subsystem_b.component:
                        ##couplings.append(Sea.model.
                        ##couplings_tuples.append((subsystem_a, subsystem_b))                        
            ##obj.PossibleRoutes = routes
            ##obj.Routes = self.model.routes
    
    def execute(self, obj):
        baseclasses.BaseClass.execute(self, obj)
        
    
    
    
        
