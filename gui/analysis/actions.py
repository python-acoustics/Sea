from PyQt4 import QtCore, QtGui

import FreeCADGui as Gui
import FreeCAD as App
import logging



class RunAnalysis:
    """
    Perform the SEA analysis. Solve the modal energies.
    """
    
    def Activated(self):
        import Sea
        if App.ActiveDocument is not None:
            if App.ActiveDocument.ActiveObject:
                Sea.actions.solve(App.ActiveDocument.ActiveObject)
            else:
                App.Console.PrintMessage('Please select an SEA system.\n')
        else:
            App.Console.PrintMessage('First create a model.\n')
         
        
    def GetResources(self):
        MenuText = QtCore.QT_TRANSLATE_NOOP('Sea_RunAnalysis', 'Start calculation')
        ToolTip  = QtCore.QT_TRANSLATE_NOOP('Sea_RunAnalysis', 'Calculate modal energies.')
        return {'Pixmap' : 'AnalysisRunIco', 'MenuText': MenuText, 'ToolTip': ToolTip} 

class StopAnalysis: 
    """
    Interrupt the calculation.
    """
    
    def Activated(self):
        import Sea
        if App.ActiveDocument is not None:
            if App.ActiveDocument.ActiveObject:
                Sea.actions.stop(App.ActiveDocument.ActiveObject)
            else:
                App.Console.PrintMessage('Please select an SEA system.\n')
        else:
            App.Console.PrintMessage('First create a model.\n')

    def GetResources(self):
        MenuText = QtCore.QT_TRANSLATE_NOOP('Sea_StopAnalysis', 'Stop calculation')
        ToolTip  = QtCore.QT_TRANSLATE_NOOP('Sea_StopAnalysis', 'Stop the currently active calculation.')
        return {'Pixmap' : 'AnalysisStopIco', 'MenuText': MenuText, 'ToolTip': ToolTip} 

class ClearAnalysis:
    """
    Clear the results of the analysis.
    """
    def Activated(self):
        import Sea
        Sea.actions.analysis.clear()

    def GetResources(self):
        MenuText = QtCore.QT_TRANSLATE_NOOP('Sea_ClearAnalysis', 'Clear results')
        ToolTip  = QtCore.QT_TRANSLATE_NOOP('Sea_ClearAnalysis', 'Delete the stored results of the analysis.')
        return {'Pixmap' : 'AnalysisPostIco', 'MenuText': MenuText, 'ToolTip': ToolTip} 


 
        
        

Gui.addCommand('Sea_RunAnalysis', RunAnalysis())
Gui.addCommand('Sea_StopAnalysis', StopAnalysis())
Gui.addCommand('Sea_ClearAnalysis', ClearAnalysis())


