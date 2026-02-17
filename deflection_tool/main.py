import argparse
import sys
import os

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
        input_parser = InputParser(args.config)
        beam = input_parser.parse()
        
        print(f"Material: {beam.material.name} (E={beam.material.E/1e9:.1f} GPa)")
        print(f"Profile: {beam.profile.type} (I={beam.profile.I:.2e} m^4)")
        
        # 2. Solve
        print("Solving for deflection...")
        solver = Solver(beam)
        solver.solve()
        
        # 3. Output Results
        print("\nResults:")
        import numpy as np
        max_deflection = np.max(np.abs(solver.deflection))
        max_idx = np.argmax(np.abs(solver.deflection))
        location = solver.x[max_idx]
        
        print(f"Maximum Deflection: {max_deflection*1000:.4f} mm at x = {location:.3f} m")
        print("Solver calculation complete.")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
