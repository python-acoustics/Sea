
import os
import Paths

from PyQt4 import QtGui,QtCore
import FreeCADGui as Gui
import FreeCAD as App

import Sea

class TaskPanelComponent(object):
    """
    Taskpanel for adding a component defined in :mod:`Sea.adapter.components`.
    """
    
    def __init__(self):
        self.ui = os.path.join(Paths.uiPath(), 'AddComponent.ui')

    
    def getObjectFromList(self, lst):
        if lst.currentItem():
            item = str(lst.currentItem().text())
            if not App.ActiveDocument:
                App.newDocument()
            return App.ActiveDocument.getObject(item)
        else:
            return None
    
    def get_sort(self):
        if self.form.sort_list.currentItem():
            return self.sort[str(self.form.sort_list.currentItem().text())]
        else:
            return None
        
    def accept(self):
        sort = self.get_sort()

        system = self.getObjectFromList(self.form.system_list)
        part = self.getObjectFromList(self.form.part_list)
        material = self.getObjectFromList(self.form.material_list)
        
        if sort:
            Sea.actions.makeComponent(sort, system, material, part)
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
        
        form.groupbox = form.findChild(QtGui.QGroupBox, 'groupBox')
        form.sort_list = form.findChild(QtGui.QListWidget, "sortList")
        form.system_list = form.findChild(QtGui.QListWidget, "systemList")
        form.part_list = form.findChild(QtGui.QListWidget, "partList")
        form.material_list = form.findChild(QtGui.QListWidget, "materialList")

        
        sort = dict()
        for key, item in Sea.adapter.components_map.iteritems():
            QtGui.QListWidgetItem(item.name, form.sort_list).setToolTip(item.description)
            sort[item.name] = key
 
        self.sort = sort
        
        if App.ActiveDocument:   
            for item in App.ActiveDocument.Objects:
                if 'IsSeaSystem' in item.PropertiesList:
                    if getattr(item, 'IsSeaSystem') == True:
                        QtGui.QListWidgetItem(item.Name, form.system_list)
                
                elif 'IsSeaMaterial' in item.PropertiesList:
                    if getattr(item, 'IsSeaMaterial') == True:
                        QtGui.QListWidgetItem(item.Name, form.material_list)
                
                else:
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
    panel = TaskPanelComponent()
    Gui.Control.showDialog(panel)
    if panel.setupUi():
        Gui.Control.closeDialog(panel)
        return None
    return panel

    