from .materials import Material
from .profiles import Profile

class Beam:
    def __init__(self, length, material, profile, supports=None):
        self.length = length
        
        # Load Material
        if isinstance(material, dict) or isinstance(material, str):
            self.material = Material(material)
        else:
            self.material = material  # Assume already a Material object
            
        # Load Profile
        if isinstance(profile, dict):
             # Expects {'type': '...', 'dimensions': {...}}
             self.profile = Profile(profile['type'], profile['dimensions'])
        else:
             self.profile = profile

        self.supports = supports if supports else []
        self.loads = []

    def add_load(self, load):
        self.loads.append(load)

    @property
    def E(self):
        return self.material.E

    @property
    def I(self):
        return self.profile.I
        
    @property
    def J(self):
        return self.profile.J

    @property
    def G(self):
        return self.material.G
        
    @property
    def y_max(self):
        return self.profile.y_max
