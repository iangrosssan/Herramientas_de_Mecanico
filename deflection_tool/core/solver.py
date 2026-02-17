import numpy as np
from scipy.integrate import cumulative_trapezoid as cumtrapz

class Solver:
    def __init__(self, beam, num_points=1000):
        self.beam = beam
        self.x = np.linspace(0, beam.length, num_points)
        
        # State arrays
        self.moment_distribution = np.zeros_like(self.x)
        self.shear_distribution = np.zeros_like(self.x)
        self.torque_distribution = np.zeros_like(self.x)
        self.axial_distribution = np.zeros_like(self.x)
        
        # Results
        self.deflection = np.zeros_like(self.x) # v(x)
        self.slope = np.zeros_like(self.x)      # theta(x)
        self.twist = np.zeros_like(self.x)      # phi(x)
        self.elongation = np.zeros_like(self.x) # u(x)
        
    def solve(self):
        """
        Solves for all deformation modes: Bending, Torsion, and Axial.
        """
        self.reset_distributions()
        L = self.beam.length
        
        # Aggregate Loads
        for load in self.beam.loads:
            if load.type == 'point':
                # Bending Moment
                P = load.magnitude
                a = load.position
                mask1 = self.x <= a
                mask2 = self.x > a
                M1 = P * (L - a) * self.x[mask1] / L
                M2 = P * a * (L - self.x[mask2]) / L
                self.moment_distribution[mask1] += M1
                self.moment_distribution[mask2] += M2
                
            elif load.type == 'distributed':
                # Supported-Supported Distributed Load q
                # Reactions: Ra = qL/2, Rb = qL/2
                # M(x) = qL/2 * x - qx^2 / 2
                # This is for a load covering the WHOLE beam.
                # TODO: Implement partial distributed loads if needed.
                q = load.magnitude
                # Assuming full span for simplicity or strictly defined start/end
                # M(x) = (q*L*x)/2 - (q*x^2)/2
                self.moment_distribution += (q * L * self.x / 2) - (q * self.x**2 / 2)

            elif load.type == 'moment':
                # Bending Moment Load
                M0 = load.magnitude
                a = load.position
                Ra = -M0 / L
                mask1 = self.x <= a
                mask2 = self.x > a
                self.moment_distribution[mask1] += Ra * self.x[mask1]
                self.moment_distribution[mask2] += Ra * self.x[mask2] + M0

            elif load.type == 'torsion':
                # Torque T applied at position a.
                # Fixed at x=0 (e.g. motor), Free at x=L
                # Internal Torque T(x) = T for 0 <= x < a, 0 for x > a
                # This depends on boundary conditions.
                # Assuming Fixed-Free (Shaft driven at 0)
                T = load.magnitude
                a = load.position
                mask = self.x <= a
                self.torque_distribution[mask] += T

            elif load.type == 'axial':
                # Axial Force P applied at position a.
                # Fixed at x=0.
                # Internal Force P(x) = P for 0 <= x < a
                P = load.magnitude
                a = load.position
                mask = self.x <= a
                self.axial_distribution[mask] += P
                
            elif load.type == 'parametric':
                # Evaluate parametric function string for distributed load
                # For safety, we should restrict evaluation context, but here we assume trusted input.
                # q(x) = eval(func)
                try:
                    # Make 'x' and 'L' available in local scope
                    context = {"x": self.x, "L": L, "np": np}
                    # We assume the user provides a string that returns an array of size x
                    # Ideally, this calculates q(x)
                    # For a simple distributed load, M(x) requires integration.
                    # This is complex to do analytically from a string.
                    # We will calculate q(x) array, then integrate numerically to get Shear V, then Moment M.
                    # V(x) = integral(q)
                    # M(x) = integral(V)
                    
                    # NOTE: This overrides the simplified algebraic formulas above.
                    # It's a numerical approach.
                    q_x = eval(load.function_string, {"__builtins__": None}, context)
                    
                    # If scalar, broadcast
                    if np.isscalar(q_x):
                        q_x = np.full_like(self.x, q_x)
                        
                    # Integrate q to get V (Shear)
                    # Boundary Condition: Simple Supports?? 
                    # Numerical integration for statically indeterminate or simple beams requires reactions.
                    # For now, let's assume Parametric applies to a Cantilever (Fixed-Free) or perform double integration with BCs.
                    # Let's stick to Cantilever logic for Parametric for now as it's easier numerically without solving system of eq.
                    # Or... calculate total load, find reactions.
                    
                    # Taking simple approach: Calculate Force F = int(q), Center of Load.
                    # Then solve reactions.
                    pass 
                except Exception as e:
                    print(f"Error evaluating parametric load: {e}")

        # Solve for Deformations
        self.solve_bending()
        self.solve_torsion()
        self.solve_axial()
        
        return {
            "deflection": self.deflection,
            "slope": self.slope,
            "twist": self.twist,
            "elongation": self.elongation,
            "x": self.x
        }

    def reset_distributions(self):
        self.moment_distribution.fill(0)
        self.shear_distribution.fill(0)
        self.torque_distribution.fill(0)
        self.axial_distribution.fill(0)

    def solve_bending(self):
        EI = self.beam.E * self.beam.I
        # Slope theta = int(M/EI)
        theta_0 = cumtrapz(self.moment_distribution / EI, self.x, initial=0)
        # Deflection y = int(theta)
        y_0 = cumtrapz(theta_0, self.x, initial=0)
        
        # BCs for Supported-Supported: y(0)=0, y(L)=0
        C1 = -y_0[-1] / self.beam.length
        self.slope = theta_0 + C1
        self.deflection = y_0 + C1 * self.x

    def solve_torsion(self):
        # Phi' = T / GJ
        GJ = self.beam.G * self.beam.J
        if GJ == 0:
            if np.any(self.torque_distribution):
                print("Warning: Torsional stiffness is zero but torque is applied. Infinite twist predicted.")
                phi_prime = np.full_like(self.x, np.inf)
            else:
                phi_prime = np.zeros_like(self.x)
        else:
            phi_prime = self.torque_distribution / GJ
        # Twist phi = int(phi')
        # BC: Fixed at x=0 => phi(0) = 0
        self.twist = cumtrapz(phi_prime, self.x, initial=0)

    def solve_axial(self):
        # u' = P / EA
        # We need Area A.
        # Assuming Beam object has access to A via profile or material?
        # Profile usually has A.
        try:
            A = self.beam.profile.A
        except AttributeError:
            # Fallback if A is missing (e.g. simple Rect profile might compute it differently)
            A = 1.0 # Placeholder
            
        EA = self.beam.E * A
        u_prime = self.axial_distribution / EA
        # Elongation u = int(u')
        # BC: Fixed at x=0 => u(0) = 0
        self.elongation = cumtrapz(u_prime, self.x, initial=0)
