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

    def moment_contribution(self, x, L):
        # Moment M(x) caused by a point load P at position 'a'
        # For a simply supported beam, reaction forces must be calculated first.
        # However, for general superposition, it's easier to handle this in the solver
        # by aggregating all loads.
        # This method might just return the raw load info for the solver to use.
        pass

class DistributedLoad(Load):
    def __init__(self, start_pos, end_pos, magnitude):
        super().__init__(start_pos, magnitude, "distributed")
        self.end_pos = end_pos

class MomentLoad(Load):
    def __init__(self, position, magnitude, axis='z'):
         super().__init__(position, magnitude, "moment")
         self.axis = axis
