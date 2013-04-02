"""
Actions related to :class:`Sea.adapter.system.System`.
"""

import Sea
import Part

import logging
import itertools

import FreeCAD as App


class System(object):
    """
    Class with public methods to manipulate :class:`Sea.adapter.system.System`.
    """
    
    def __init__(self, obj):
        
        
        if Sea.actions.document.isSystem(obj):
            self.system = obj
        else:
            App.Console.PrintError('Invalid DocumentObject.\n')
            raise ValueError

    