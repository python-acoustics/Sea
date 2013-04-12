"""
The following are Material classes encapsulating their respective :mod:`Sea.model.materials` class.
"""


from MaterialGas import MaterialGas
from MaterialSolid import MaterialSolid

from ViewProviderMaterial import ViewProviderMaterial

    
import inspect, sys
materials_map = {item[0]: item[1] for item in inspect.getmembers(sys.modules[__name__], inspect.isclass)}
"""
Dictionary with all available materials.
"""