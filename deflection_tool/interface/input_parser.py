import json
from ..core.beam import Beam
from ..core.loads import PointLoad, DistributedLoad, MomentLoad, TorsionLoad, AxialLoad, ParametricLoad

class InputParser:
    @staticmethod
    def parse_json(file_path):
        with open(file_path, 'r') as f:
            data = json.load(f)
            
        # Parse Geometry & Material
        length = data.get('geometry', {}).get('length', 1.0)
        material = data.get('material')
        profile = data.get('geometry', {}).get('cross_section_data', {})
        
        # If simple cross_section string is provided, mapping needed
        # Assuming the JSON structure is like {'geometry': {'cross_section': 'circular', 'dimensions': {...}}}
        # Let's adjust to match common usage
        geo = data.get('geometry', {})
        if 'cross_section' in geo:
            start_profile = {
                'type': geo['cross_section'],
                'dimensions': geo.get('dimensions', {})
            }
        else:
            start_profile = profile

        beam = Beam(length, material, start_profile)
        
        # Parse Loads
        for load_data in data.get('loads', []):
            l_type = load_data.get('type')
            
            if l_type == 'point_load':
                beam.add_load(PointLoad(
                    position=load_data['position'],
                    magnitude=load_data['magnitude'],
                    direction=load_data.get('direction', 'y')
                ))
            elif l_type == 'distributed_load':
                beam.add_load(DistributedLoad(
                    start_pos=load_data.get('start', 0),
                    end_pos=load_data.get('end', length),
                    magnitude=load_data['magnitude']
                ))
            elif l_type == 'moment_load':
                beam.add_load(MomentLoad(
                    position=load_data['position'],
                    magnitude=load_data['magnitude']
                ))
            elif l_type == 'torsion_load':
                beam.add_load(TorsionLoad(
                    position=load_data['position'],
                    magnitude=load_data['magnitude']
                ))
            elif l_type == 'axial_load':
                beam.add_load(AxialLoad(
                    position=load_data['position'],
                    magnitude=load_data['magnitude']
                ))
            elif l_type == 'parametric_load':
                beam.add_load(ParametricLoad(
                    start_pos=load_data.get('start', 0),
                    end_pos=load_data.get('end', length),
                    function_string=load_data['function']
                ))
                
        return beam
