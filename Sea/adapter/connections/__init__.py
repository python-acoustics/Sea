"""
Module with the different types of Connections that are available.
"""


from ConnectionPoint import ConnectionPoint
from ConnectionLine import ConnectionLine
from ConnectionSurface import ConnectionSurface


import inspect, sys
connections_map = {item[0]: item[1] for item in inspect.getmembers(sys.modules[__name__], inspect.isclass)}
"""
Dictionary with all available excitations.
"""