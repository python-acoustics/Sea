
import numpy as np

class Frequency(object):
    """
    Abstract base class for handling different frequency settings.
    """
    
    
    center = np.array([0.0])
    """
    Center frequencies of frequency bands.
    """
    lower = np.array([0.0])
    """
    Lower limit frequencies of frequency bands.
    """
    upper = np.array([0.0])
    """
    Upper limit frequencies of frequency bands.
    """
    
    enabled = np.array([False])
    """
    Enabled frequency bands.
    
    Modal powers will not be solved for disabled frequency bands.
    """
    
    @property
    def bandwidth(self):
        """Bandwidth of frequency bands,
        
        :rtype: :class:`numpy.ndarray`
        """
        return self.upper - self.lower

    @property
    def angular(self):
        """Angular frequency
        
        :rtype: :class:`numpy.ndarray`
        """
        return self.center * 2.0 * np.pi 
        
    @property
    def amount(self):
        """Amount of frequency bands
        
        :rtype: :func:`int`
        """
        try:
            return len(self.center)
        except TypeError:
            return 0