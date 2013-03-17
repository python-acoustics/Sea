"""
Subsystems are connected to eachother through couplings.
"""

from coupling_1D_structural import Coupling1DStructural
from coupling_2D_structural import Coupling2DStructural

from coupling_3D_platecavity import Coupling3DPlateCavity
from coupling_3D_cavityplate import Coupling3DCavityPlate



import inspect, sys
couplings_map = {item[0]: item[1] for item in inspect.getmembers(sys.modules[__name__], inspect.isclass)}
"""
Dictionary with all available couplings.
"""