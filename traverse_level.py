import unreal
import os
import sys

path = r'C:\Projects\ContentTracker'
if path not in sys.path:
    sys.path.append(path)


from utils_unreal import get_meshes_by_class


def get_map_static_meshes(map_):
    map_assets = fr'C:\p4vSDevMinNSA\MK12\Content\Disk\Env\{map_}\Asset'

    data = {}
    asset_dirs = os.listdir(map_assets)[:5]
    for asset_dir in asset_dirs:
        if os.path.isdir(os.path.join(map_assets, asset_dir)):
            data[asset_dir] = {}
            path = fr'/Game/Disk/Env/{map_}/Asset/{asset_dir}'
            data[asset_dir] = get_meshes_by_class(path, unreal.StaticMesh)
    
    return data
        

def print_sm_data(data):
    for k,v in data.items():
        print(f'{k}\n')
        print([val.get_name() for val in v])


data = get_map_static_meshes('TeaHouse')
print_sm_data(data)