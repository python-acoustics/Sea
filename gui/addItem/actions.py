import FreeCADGui as Gui

from PyQt4 import QtGui,QtCore


import TaskPanel

class AddSystem: 
    def Activated(self):
        import TaskPanelAddSystem
        TaskPanelAddSystem.load()

    def GetResources(self):
        MenuText = QtCore.QT_TRANSLATE_NOOP('Sea_AddSystem', 'System')
        ToolTip  = QtCore.QT_TRANSLATE_NOOP('Sea_AddSystem', 'Add a new system.')
        return {'Pixmap' : 'AnalysisCreateIco', 'MenuText': MenuText, 'ToolTip': ToolTip} 
        
class AddComponent: 
    def Activated(self):
        import TaskPanelAddComponent
        TaskPanelAddComponent.load()

    def GetResources(self):
        MenuText = QtCore.QT_TRANSLATE_NOOP('Sea_AddComponent', 'Component')
        ToolTip  = QtCore.QT_TRANSLATE_NOOP('Sea_AddComponent', 'Add a new component.')
        return {'Pixmap' : 'AnalysisCreateIco', 'MenuText': MenuText, 'ToolTip': ToolTip} 
        
class AddSubsystem: 
    def Activated(self):
        import TaskPanelAddSubsystem
        TaskPanelAddSubsystem.load()

    def GetResources(self):
        MenuText = QtCore.QT_TRANSLATE_NOOP('Sea_AddSubsystem', 'Subsystem')
        ToolTip  = QtCore.QT_TRANSLATE_NOOP('Sea_AddSubsystem', 'Add a new subsystem.')
        return {'Pixmap' : 'AnalysisCreateIco', 'MenuText': MenuText, 'ToolTip': ToolTip} 
              
class AddCoupling: 
    def Activated(self):
        import TaskPanelAddCoupling
        TaskPanelAddCoupling.load()

    def GetResources(self):
        MenuText = QtCore.QT_TRANSLATE_NOOP('Sea_AddCoupling', 'Coupling')
        ToolTip  = QtCore.QT_TRANSLATE_NOOP('Sea_AddCoupling', 'Add a new coupling.')
        return {'Pixmap' : 'AnalysisCreateIco', 'MenuText': MenuText, 'ToolTip': ToolTip} 

class AddExcitation: 
    def Activated(self):
        import TaskPanel
        TaskPanel.add_excitation()

    def GetResources(self):
        MenuText = QtCore.QT_TRANSLATE_NOOP('Sea_AddExcitation', 'Excitation')
        ToolTip  = QtCore.QT_TRANSLATE_NOOP('Sea_AddExcitation', 'Add a new excitation.')
        return {'Pixmap' : 'AnalysisCreateIco', 'MenuText': MenuText, 'ToolTip': ToolTip}     
        
class AddMaterial: 
    def Activated(self):
        import TaskPanel
        TaskPanel.add_material()

    def GetResources(self):
        MenuText = QtCore.QT_TRANSLATE_NOOP('Sea_AddMaterial', 'Material')
        ToolTip  = QtCore.QT_TRANSLATE_NOOP('Sea_AddMaterial', 'Add a new material.')
        return {'Pixmap' : 'AnalysisCreateIco', 'MenuText': MenuText, 'ToolTip': ToolTip} 


Gui.addCommand('Sea_AddSystem', AddSystem())  
Gui.addCommand('Sea_AddComponent', AddComponent())
Gui.addCommand('Sea_AddSubsystem', AddSubsystem())
Gui.addCommand('Sea_AddCoupling', AddCoupling())
Gui.addCommand('Sea_AddExcitation', AddExcitation())
Gui.addCommand('Sea_AddMaterial', AddMaterial())