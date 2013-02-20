
import os
import Paths

from PyQt4 import QtGui,QtCore
import FreeCADGui as Gui
import FreeCAD as App

import Sea

class TaskPanel(object):

    def __init__(self):
        self.ui = os.path.join(Paths.uiPath(), 'AddSystem.ui')

        
    def accept(self):
        
        build = self.form.build.isChecked()
        
        if not App.ActiveDocument:
            App.newDocument()
        document = App.ActiveDocument
        
        if build:
            Sea.actions.create_system_from_document(document)
        else:
            Sea.actions.create_empty_system(document)
            
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
        
        form.build = form.findChild(QtGui.QCheckBox, 'buildSystem')
        
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
    panel = TaskPanel()
    Gui.Control.showDialog(panel)
    if panel.setupUi():
        Gui.Control.closeDialog(panel)
        return None
    return panel

    