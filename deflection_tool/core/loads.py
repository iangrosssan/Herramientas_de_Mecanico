import numpy as np

class Load:
    def __init__(self, position, magnitude=0, load_type="point"):
        self.position = position
        self.magnitude = magnitude
        self.type = load_type

    def apply(self, x, L):
        """
        Calculate the contribution of this load to the moment/force distribution at position x.
        This base method should be overridden.
        """
        pass

class PointLoad(Load):
    def __init__(self, position, magnitude, direction='y'):
        super().__init__(position, magnitude, "point")
        self.direction = direction

class DistributedLoad(Load):
    def __init__(self, start_pos, end_pos, magnitude):
        super().__init__(start_pos, magnitude, "distributed")
        self.end_pos = end_pos

class MomentLoad(Load):
    def __init__(self, position, magnitude, axis='z'):
         super().__init__(position, magnitude, "moment")
         self.axis = axis

class TorsionLoad(Load):
    """
    Torque T applied at a specific position.
    """
    def __init__(self, position, magnitude):
        super().__init__(position, magnitude, "torsion")

class AxialLoad(Load):
    """
    Axial force P applied at a specific position.
    Positive magnitude = Tension? (Convention needs to be defined in solver)
    """
    def __init__(self, position, magnitude):
        super().__init__(position, magnitude, "axial")

class ParametricLoad(Load):
    """
    Distributed load defined by a function string (e.g., '100*x' or 'sin(x)').
    """
    def __init__(self, start_pos, end_pos, function_string):
        # Magnitude is dynamic, so we might store 0 or max/avg
        super().__init__(start_pos, 0, "parametric")
        self.end_pos = end_pos
        self.function_string = function_string
