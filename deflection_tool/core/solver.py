import numpy as np
from scipy.integrate import cumulative_trapezoid as cumtrapz

class Solver:
    def __init__(self, beam, num_points=1000):
        self.beam = beam
        self.x = np.linspace(0, beam.length, num_points)
        self.moment_distribution = np.zeros_like(self.x)
        self.shear_distribution = np.zeros_like(self.x)
        self.deflection = np.zeros_like(self.x)
        self.slope = np.zeros_like(self.x)
        
    def solve(self):
        """
        Solves for deflection by integrating the Moment distribution.
        Starting with a simplified case for Supported-Supported beams.
        """
        # Initialize Moment Distribution
        self.moment_distribution = np.zeros_like(self.x)
        L = self.beam.length
        
        # Superposition of Moments
        for load in self.beam.loads:
            if load.type == 'point':
                # Simplified Moment for Point Load P at position 'a' on Simply Supported Beam
                # M(x) = P(L-a)x/L  for 0 <= x <= a
                # M(x) = Pa(L-x)/L  for a < x <= L
                P = load.magnitude
                a = load.position
                
                # Careful with numpy arrays
                mask1 = self.x <= a
                mask2 = self.x > a
                
                M1 = P * (L - a) * self.x[mask1] / L
                M2 = P * a * (L - self.x[mask2]) / L
                
                self.moment_distribution[mask1] += M1
                self.moment_distribution[mask2] += M2
                
            elif load.type == 'distributed':
                # Placeholder for distributed load moment
                pass
                
            elif load.type == 'moment':
                # Simplified Moment for Moment Load M0 at position 'a'
                # Reactions: Ra = -M0/L, Rb = M0/L
                # M(x) = Ra * x          for 0 <= x < a
                # M(x) = Ra * x + M0     for a < x <= L
                M0 = load.magnitude
                a = load.position
                
                Ra = -M0 / L
                
                mask1 = self.x <= a
                mask2 = self.x > a
                
                M1 = Ra * self.x[mask1]
                M2 = Ra * self.x[mask2] + M0
                
                self.moment_distribution[mask1] += M1
                self.moment_distribution[mask2] += M2

        return self.integrate_moment(self.moment_distribution)

    def integrate_moment(self, M_x):
        """
        Given the moment distribution M(x), calculate slope and deflection.
        Ex: theta = integral(M / EI) + C1
            y = integral(theta) + C2
        """
        EI = self.beam.E * self.beam.I
        
        # First Integration: Slope (theta)
        # theta_0 = integral(M/EI) from 0 to x
        theta_0 = cumtrapz(M_x / EI, self.x, initial=0)
        
        # Second Integration: Deflection (y_0)
        # y_0 = integral(theta_0) from 0 to x
        y_0 = cumtrapz(theta_0, self.x, initial=0)
        
        # Constants of Integration (Boundary Conditions)
        # For Supported-Supported (y(0)=0, y(L)=0):
        # y(x) = y_0(x) + C1*x + C2
        # y(0) = 0 => 0 + 0 + C2 = 0 => C2 = 0
        # y(L) = y_0(L) + C1*L = 0 => C1 = -y_0(L) / L
        
        C2 = 0
        C1 = -y_0[-1] / self.beam.length
        
        self.slope = theta_0 + C1
        self.deflection = y_0 + C1 * self.x + C2
        
        return self.deflection
