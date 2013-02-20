

import FreeCAD, FreeCADGui, os

def modulePath():
    path1 = os.path.join(FreeCAD.ConfigGet("AppHomePath"), 'Mod', 'Sea')
    path2 = os.path.join(FreeCAD.ConfigGet("UserAppData"), 'Mod', 'Sea')
    if os.path.exists(path2):
        return path2
    else:
        return path1
        
def resourcesPath():
    return os.path.join(modulePath(), 'resources')
    
def examples():
    return os.path.join(resourcesPath(), 'examples')
      
def iconsPath():
    return os.path.join(resourcesPath(), 'icons')
    
def translationsPath():
    return os.path.join(resourcesPath(), 'translations')
    
def uiPath():
    return os.path.join(resourcesPath(), 'ui')