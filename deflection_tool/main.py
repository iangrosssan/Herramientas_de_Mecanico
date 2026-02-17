import argparse
import sys
import os
import numpy as np

# Add the parent directory to sys.path so we can import the package
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from deflection_tool.interface.input_parser import InputParser
from deflection_tool.core.solver import Solver

def main():
    parser = argparse.ArgumentParser(description="Mechanical Deflection Analysis Tool")
    parser.add_argument('config', help='Path to the JSON configuration file')
    args = parser.parse_args()

    try:
        # 1. Parse Input
        print(f"Loading configuration from {args.config}...")
        # Updated to use static method per new InputParser implementation
        beam = InputParser.parse_json(args.config)
        
        print(f"Material: {beam.material.name} (E={beam.material.E/1e9:.1f} GPa, G={beam.material.G/1e9:.1f} GPa)")
        print(f"Profile: {beam.profile.type}")
        print(f"  I = {beam.profile.I:.2e} m^4")
        if hasattr(beam.profile, 'J'):
            print(f"  J = {beam.profile.J:.2e} m^4")
        if hasattr(beam.profile, 'A'):
            print(f"  A = {beam.profile.A:.2e} m^2")
        
        # 2. Solve
        print("Solving for generalized deformations...")
        solver = Solver(beam)
        results = solver.solve()
        
        # 3. Output Results
        print("\nResults:")
        
        # Bending
        max_defl = np.max(np.abs(results['deflection']))
        loc_defl = solver.x[np.argmax(np.abs(results['deflection']))]
        print(f"  Max Bending Deflection (v): {max_defl*1000:.4f} mm at x={loc_defl:.3f} m")
        
        # Slope
        max_slope = np.max(np.abs(results['slope']))
        print(f"  Max Slope (theta): {np.degrees(max_slope):.4f} deg")

        # Torsion
        if np.any(results['twist']):
            max_twist = np.max(np.abs(results['twist']))
            print(f"  Max Twist (phi): {np.degrees(max_twist):.4f} deg")
        else:
            print("  Max Twist (phi): 0.0000 deg (No Torsion Load)")

        # Axial
        if np.any(results['elongation']):
            max_axial = np.max(np.abs(results['elongation']))
            print(f"  Max Axial Displacement (u): {max_axial*1000:.4f} mm")
        else:
            print("  Max Axial Displacement (u): 0.0000 mm (No Axial Load)")

        print("Calculation complete.")

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
