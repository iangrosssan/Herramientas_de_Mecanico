import json
from ..core.beam import Beam
from ..core.loads import PointLoad, DistributedLoad, MomentLoad

class InputParser:
    def __init__(self, json_file):
        self.json_file = json_file
        self.data = self._load()

    def _load(self):
        with open(self.json_file, 'r') as f:
            return json.load(f)

    def parse(self):
        """
        Parses the JSON data and returns a configured Beam object and Loads.
        """
        # 1. Create Beam
        # Material can be string (DB) or dict (Custom)
        material = self.data['material']
        
        # Profile
        profile_data = self.data['geometry']['cross_section']
        # If string 'circular', we expect dimensions to be there
        if isinstance(profile_data, str):
            profile = {
                'type': profile_data,
                'dimensions': self.data['geometry']['dimensions']
            }
        else:
            profile = profile_data

        length = self.data['geometry']['length']
        
        supports = self.data.get('supports', []) # Keep raw for now
        
        beam = Beam(length, material, profile, supports)
        
        # 2. Add Loads
        if 'loads' in self.data:
            for load_data in self.data['loads']:
                load_type = load_data['type']
                if load_type == 'point_load':
                    load = PointLoad(load_data['position'], load_data['magnitude'])
                elif load_type == 'moment':
                    load = MomentLoad(load_data['position'], load_data['magnitude'])
                # Add other types
                beam.add_load(load)
                
        return beam
