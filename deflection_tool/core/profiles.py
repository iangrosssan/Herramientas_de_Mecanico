import numpy as np

class Profile:
    def __init__(self, type_name, dimensions):
        self.type = type_name
        self.dimensions = dimensions
        self.I = 0
        self.J = 0
        self.A = 0
        self.y_max = 0
        self.shear_correction = 0 # Shear correction factor
        
        self._calculate_properties()
        
    def _calculate_properties(self):
        if self.type == 'circular':
            d = self.dimensions['diameter']
            r = d / 2
            self.A = np.pi * r**2
            self.I = np.pi * r**4 / 4
            self.J = np.pi * r**4 / 2
            self.y_max = r
            self.shear_correction = 1.33 # For circular solid
            
        elif self.type == 'rectangular':
            b = self.dimensions['width']
            h = self.dimensions['height']
            self.A = b * h
            self.I = b * h**3 / 12
            # J for rectangular is complex, approximation or use standard formulas
            # For simplicity, we might need a specific calculation or ignore torsion if not needed
            # For now, let's use a placeholder or raise not implemented for torsion on rect
            self.y_max = h / 2
            self.shear_correction = 1.2 # For rectangular
            
        else:
            raise ValueError(f"Unknown profile type: {self.type}")
