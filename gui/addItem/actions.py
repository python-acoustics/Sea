"""
Actions
"""
import FreeCAD as App
import FreeCADGui as Gui

from PyQt4 import QtGui,QtCore

class AddSystem(object):
    """
    Open taskpanel in order to add a :class:`Sea.adapter.system.System`.
    """
    def Activated(self):
        if App.ActiveDocument:
            import TaskPanelAddSystem
            TaskPanelAddSystem.load()
        else:
            App.Console.PrintWarning('Please create a document first.\n')
            
    def GetResources(self):
        MenuText = QtCore.QT_TRANSLATE_NOOP('Sea_AddSystem', 'System')
        ToolTip  = QtCore.QT_TRANSLATE_NOOP('Sea_AddSystem', 'Add a new system.')
        return {'Pixmap' : 'AnalysisCreateIco', 'MenuText': MenuText, 'ToolTip': ToolTip} 
        
class AddComponent(object): 
    """
    Open taskpanel in order to add an object from :mod:`Sea.adapter.components`.
    """
    def Activated(self):
        if App.ActiveDocument:
            import TaskPanelAddComponent
            TaskPanelAddComponent.load()
        else:
            App.Console.PrintWarning('Please create a document first.\n')
            
    def GetResources(self):
        MenuText = QtCore.QT_TRANSLATE_NOOP('Sea_AddComponent', 'Component')
        ToolTip  = QtCore.QT_TRANSLATE_NOOP('Sea_AddComponent', 'Add a new component.')
        return {'Pixmap' : 'AnalysisCreateIco', 'MenuText': MenuText, 'ToolTip': ToolTip} 
                      
#class AddCoupling(object): 
    #"""
    #Open taskpanel in order to add an object from :mod:`Sea.adapter.couplings`.
    #"""
    #def Activated(self):
        #import TaskPanelAddCoupling
        #TaskPanelAddCoupling.load()

    #def GetResources(self):
        #MenuText = QtCore.QT_TRANSLATE_NOOP('Sea_AddCoupling', 'Coupling')
        #ToolTip  = QtCore.QT_TRANSLATE_NOOP('Sea_AddCoupling', 'Add a new coupling.')
        #return {'Pixmap' : 'AnalysisCreateIco', 'MenuText': MenuText, 'ToolTip': ToolTip} 

class AddExcitation(object):
    """
    Open taskpanel in order to add an object from :mod:`Sea.adapter.excitations`.
    """
    def Activated(self):
        if App.ActiveDocument:
            import TaskPanelAddExcitation
            TaskPanelAddExcitation.load()
        else:
            App.Console.PrintWarning('Please create a document first.\n')
            
    def GetResources(self):
        MenuText = QtCore.QT_TRANSLATE_NOOP('Sea_AddExcitation', 'Excitation')
        ToolTip  = QtCore.QT_TRANSLATE_NOOP('Sea_AddExcitation', 'Add a new excitation.')
        return {'Pixmap' : 'AnalysisCreateIco', 'MenuText': MenuText, 'ToolTip': ToolTip}     
        
class AddMaterial(object):
    """
    Open taskpanel in order to add an object from :mod:`Sea.adapter.materials`.
    """
    def Activated(self):
        if App.ActiveDocument:
            import TaskPanelAddMaterial
            TaskPanelAddMaterial.load()
        else:
            App.Console.PrintWarning('Please create a document first.\n')
            
    def GetResources(self):
        MenuText = QtCore.QT_TRANSLATE_NOOP('Sea_AddMaterial', 'Material')
        ToolTip  = QtCore.QT_TRANSLATE_NOOP('Sea_AddMaterial', 'Add a new material.')
        return {'Pixmap' : 'AnalysisCreateIco', 'MenuText': MenuText, 'ToolTip': ToolTip} 


      
Gui.addCommand('Sea_AddSystem', AddSystem())  
Gui.addCommand('Sea_AddComponent', AddComponent())
#Gui.addCommand('Sea_AddConnection', AddConnection())
#Gui.addCommand('Sea_AddCoupling', AddCoupling())
Gui.addCommand('Sea_AddExcitation', AddExcitation())
Gui.addCommand('Sea_AddMaterial', AddMaterial())