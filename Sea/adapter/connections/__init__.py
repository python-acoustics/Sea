"""
Module with the different types of Connections that are available.
"""


from connection_point import ConnectionPoint
from connection_line import ConnectionLine
from connection_surface import ConnectionSurface


import inspect, sys
connections_map = {item[0]: item[1] for item in inspect.getmembers(sys.modules[__name__], inspect.isclass)}
"""
Dictionary with all available excitations.
"""