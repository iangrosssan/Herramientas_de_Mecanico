from ..core.beam import Beam
from ..core.loads import PointLoad, MomentLoad
import numpy as np

class ShaftWithGears:
    def __init__(self, beam):
        self.beam = beam
        self.loads = []
        
        # This scenario is specific to the project, so parameters might be hardcoded
        # Or passed via config.
        # For now, let's assume the JSON provides the high-level gear specs
        # and this class translates them into forces/moments.
        pass

    def calculate_gear_loads(self, gears):
        """
        Takes a list of gear definitions and calculates the loads on the shaft.
        """
        for gear in gears:
            # Extract gear properties (diameters, thickness, position)
            pos = gear['position']
            mass = self._calculate_weight(gear)
            
            # 1. Gravity Load (Weight)
            gravity_load = PointLoad(pos, -mass * 9.81, 'y')
            self.beam.add_load(gravity_load)
            
            # 2. Radial/Tangential loads if provided
            if 'forces' in gear:
                # Add radial/tangential loads
                pass
                
            # 3. Torque/Moment if provided
            if 'torque' in gear:
                 pass

    def _calculate_weight(self, gear):
        # Specific formula from the notebook
        d_mm = gear['diameter']
        e_mm = gear['thickness']
        rho = self.beam.material.rho
        
        r = d_mm / 2000
        e_m = e_mm / 1000
        volume = np.pi * r**2 * e_m
        mass = rho * volume
        return mass
