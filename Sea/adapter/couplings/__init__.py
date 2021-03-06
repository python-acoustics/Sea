"""
Subsystems are connected to eachother through couplings.
"""

from Coupling1DStructural import Coupling1DStructural
from Coupling2DStructural import Coupling2DStructural

from Coupling3DPlateCavity import Coupling3DPlateCavity
from Coupling3DCavityPlate import Coupling3DCavityPlate

from ViewProviderCoupling import ViewProviderCoupling

import inspect, sys
couplings_map = {item[0]: item[1] for item in inspect.getmembers(sys.modules[__name__], inspect.isclass)}
"""
Dictionary with all available couplings.
"""