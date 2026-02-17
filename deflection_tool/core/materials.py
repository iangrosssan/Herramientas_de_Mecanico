import json
import os

class Material:
    def __init__(self, name_or_dict):
        """
        Initialize a Material object.
        
        Args:
            name_or_dict (str or dict): Either a string name of a standard material
                                      (e.g., 'AISI4140') or a dictionary of properties.
        """
        self.properties = {}
        
        if isinstance(name_or_dict, str):
            self._load_from_db(name_or_dict)
        elif isinstance(name_or_dict, dict):
            self.properties = name_or_dict
        else:
            raise ValueError("Material must be defined by a string name or a dictionary of properties.")
            
        self._validate()

    def _load_from_db(self, name):
        # Locate the materials.json file relative to this file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(current_dir, '..', 'data', 'materials.json')
        
        with open(db_path, 'r') as f:
            db = json.load(f)
            
        if name not in db:
            raise ValueError(f"Material '{name}' not found in database. Available: {list(db.keys())}")
            
        self.properties = db[name]
        self.properties['name'] = name

    def _validate(self):
        required = ['E', 'rho', 'nu'] # Young's Modulus, Density, Poisson's Ratio
        for prop in required:
            if prop not in self.properties:
                raise ValueError(f"Material definition missing required property: {prop}")
        
        # Calculate Shear Modulus G if not provided
        if 'G' not in self.properties:
            E = self.properties['E']
            nu = self.properties['nu']
            self.properties['G'] = E / (2 * (1 + nu))

    @property
    def E(self):
        return self.properties['E']

    @property
    def G(self):
        return self.properties['G']

    @property
    def rho(self):
        return self.properties['rho']
        
    @property
    def yield_strength(self):
        return self.properties.get('yield_strength', float('inf'))
    
    @property
    def name(self):
        return self.properties.get('name', 'Custom')
