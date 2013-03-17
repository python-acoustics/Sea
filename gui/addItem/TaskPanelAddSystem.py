
import os
import Paths

from PyQt4 import QtGui,QtCore
import FreeCADGui as Gui
import FreeCAD as App

import Sea

class TaskPanelAddSystem(object):
    """
    Taskpanel for adding a :class:`Sea.adapter.system.System`.
    """

    def __init__(self):
        self.ui = os.path.join(Paths.uiPath(), 'AddSystem.ui')

    
    def getObjectFromList(self, lst):
        if lst.currentItem():
            item = str(lst.currentItem().text())
            if not App.ActiveDocument:
                App.newDocument()
            return App.ActiveDocument.getObject(item)
        else:
            return None
        
    def accept(self):
        
        build = self.form.build.isChecked()
        part = self.getObjectFromList(self.form.part_list)
        
        if build:
            App.Console.PrintMessage("Creating new SEA System.\n")
            Sea.actions.document.create_system_from_structure(part)
        else:
            App.Console.PrintMessage("Creating new SEA System from geometry.\n")
            Sea.actions.document.create_empty_system(part)
            
        return True

    def reject(self):
        return True

    def clicked(self, index):
        pass

    def open(self):
        pass

    def needsFullSpace(self):
        return True

    def isAllowedAlterSelection(self):
        return False

    def isAllowedAlterView(self):
        return True

    def isAllowedAlterDocument(self):
        return False

    def helpRequested(self):
        pass

    def setupUi(self):
        mw = self.getMainWindow()
        form = mw.findChild(QtGui.QWidget, "TaskPanel")
        #form.title
        
        form.part_list = form.findChild(QtGui.QListWidget, "partList")
        form.build = form.findChild(QtGui.QCheckBox, 'buildSystem')
        
        for item in App.ActiveDocument.Objects:
            if item.isDerivedFrom('Part::MultiFuse'):
                QtGui.QListWidgetItem(item.Name, form.part_list)
           
        
        
        #form.groupbox.setTitle('Add ' + self.sort)
        #form.setWindowTitle('Add ' + self.sort)
        
        #form.label = form.findChild(QtGui.QLabel, 'label')
        #form.label.setText('Please select the type of ' + self.sort + ' you would like to add.')
        self.form = form

    def getMainWindow(self):
        "returns the main window"
        # using QtGui.qApp.activeWindow() isn't very reliable because if another
        # widget than the mainwindow is active (e.g. a dialog) the wrong widget is
        # returned
        toplevel = QtGui.qApp.topLevelWidgets()
        for i in toplevel:
            if i.metaObject().className() == "Gui::MainWindow":
                return i
        raise Exception("No main window found")


def load():
    """
    Load the taskpanel defined in this file.
    """
    panel = TaskPanelAddSystem()
    Gui.Control.showDialog(panel)
    if panel.setupUi():
        Gui.Control.closeDialog(panel)
        return None
    return panel

    