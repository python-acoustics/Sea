
class SeaWorkbench(Workbench):
    """
    Statistical Energy Analysis workbench
    """

    Icon = """
            /* XPM */
            static const char *test_icon[]={
            "16 16 2 1",
            "a c #000000",
            ". c None",
            "................",
            "................",
            "..############..",
            "..############..",
            "..############..",
            "......####......",
            "......####......",
            "......####......",
            "......####......",
            "......####......",
            "......####......",
            "......####......",
            "......####......",
            "......####......",
            "................",
            "................"};
            """
    MenuText = "SEA"
    ToolTip = "Statistical Energy Analysis workbench"
    
    def Initialize(self):
        from PyQt4 import QtCore, QtGui

        import Paths
        import gui
        import Sea
        
        Gui.addIconPath(Paths.iconsPath())
        Gui.addLanguagePath(Paths.translationsPath())


        items = ["Sea_AddSystem", "Sea_AddComponent", "Sea_AddCoupling", "Sea_AddExcitation", "Sea_AddMaterial"]
        self.appendToolbar(str(QtCore.QT_TRANSLATE_NOOP("Sea", "Add item")), items)
        self.appendMenu(str(QtCore.QT_TRANSLATE_NOOP("Sea", "Add item")), items)        
 
        
        items = ["Sea_RunAnalysis", "Sea_StopAnalysis", "Sea_ClearAnalysis"];
        self.appendToolbar(str(QtCore.QT_TRANSLATE_NOOP("Sea", "Analysis")), items)
        self.appendMenu(str(QtCore.QT_TRANSLATE_NOOP("Sea", "Analysis")), items)
        

        
        
        
        Log('Loading Sea module... done\n')
        
    def Activated(self):
        Msg("SeaWorkbench::Activated()\n")
        
    def Deactivated(self):
        Msg("SeaWorkbench::Deactivated()\n")

Gui.addWorkbench(SeaWorkbench)