import unreal
from typing import List


FOLDERS = [
        r'/Game/Disk/Env/TeaHouse/Asset/TeaHouse_Chair/Mesh',
        ]


def filter_by_class(assets) -> List[str]:
    registry = unreal.AssetRegistryHelpers.get_asset_registry()
    
    filtered = []
    for asset_path in assets:
        asset_data = registry.get_asset_by_object_path(asset_path)
        asset_class = asset_data.asset_class
        
        if asset_class == 'StaticMesh':
            filtered.append(asset_path)
    
    return filtered


def revert_mesh_lods(static_mesh: unreal.StaticMesh):
    """Removes all LODs from SMesh"""

    lod0 = unreal.EditorStaticMeshLibrary.get_lod_reduction_settings(static_mesh, 0)

    lod0.termination_criterion = unreal.StaticMeshReductionTerimationCriterion.TRIANGLES
    
    # set default lods
    options = unreal.EditorScriptingMeshReductionOptions()  
    options.reduction_settings = [unreal.EditorScriptingMeshReductionSettings(1.0, 1.0)]
    unreal.EditorStaticMeshLibrary.set_lods(static_mesh, options)

    options.auto_compute_lod_screen_size = False
    unreal.EditorStaticMeshLibrary.set_lods(static_mesh, options)
    
    unreal.EditorStaticMeshLibrary.set_lod_reduction_settings(static_mesh, 0, lod0)

    
def main(folders:List):
    for folder in folders:
        all_assets = unreal.EditorAssetLibrary.list_assets(folder, recursive=True)
        static_meshes = filter_by_class(all_assets)
        
        for smesh in static_meshes:
            loaded_smesh = unreal.load_asset(smesh)

            num_lods = loaded_smesh.get_num_lods()
            
            if num_lods > 1:
                revert_mesh_lods(loaded_smesh)
                unreal.EditorAssetLibrary.save_loaded_asset(loaded_smesh)

                print(f'============ DONE for {smesh}')


main(FOLDERS)