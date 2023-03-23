import inspect
import unreal
from typing import List

def get_selected_assets(asset_type=None):
    assets_data_list = None
    
    assets_data_list = unreal.EditorUtilityLibrary.get_selected_asset_data()
    unreal.EditorLevelLibrary.get_selected_level_actors
    unreal.EditorUtilityLibrary.get_se
    # return assets_data_list

    if asset_type:
        assets_data_list = unreal.AssetRegistryHelpers.get_asset_registry().get_assets_by_class(asset_type)
    else:
        assets_data_list = unreal.AssetRegistryHelpers.get_asset_registry().get_all_assets()
    
    return assets_data_list


def get_assets_in_folder(path: str, all_assets=False, NX=False, recursive=False) -> List[str]:
    assets = unreal.EditorAssetLibrary.list_assets(path, recursive=recursive)

    if NX:
        all_assets = False
        assets = list(filter(lambda asset:'_NX' in asset, assets))   
        return assets

    if all_assets and NX:
        raise RuntimeError(f'{inspect.current_frame.f_code.co_name} flags "all_assets" and "only_NX" are exclusive')
    
    if all_assets:
        return assets
    else:
        assets = list(filter(lambda asset:'_NX' not in asset, assets))
        return assets


def filter_by_class(assets, class_: unreal.Object) -> List[str]:
    registry = unreal.AssetRegistryHelpers.get_asset_registry()
    
    filtered = []
    for asset_path in assets:
        asset_data = registry.get_asset_by_object_path(asset_path)
        asset_class = asset_data.asset_class
        
        #TODO rewrite this
        if asset_class == 'SkeletalMesh':
            filtered.append(asset_path)
    
    return filtered


def find_original_and_NX(asset):
    def is_NX(asset_ref:str):
        return '_NX' in asset_ref

    def find_NX_for_original(asset: str):
        NX = None
        try:
            #TODO write regex
            name = asset.split('.')  # SM_TeaHouse_Chair_1.SM_TeaHouse_Chair_1
            NX = name[0] + '_NX' + '.' + name[1] + '_NX'
        except:
            print(f'Error finding original for NX mesh {asset}')

        return NX
    
    def find_original_for_NX(asset: str):
        orig = None
        try:

            #TODO write regex
            orig = asset.replace('_NX', '')
        except:
            print(f'Error finding NX duplicate for {asset}')
        
        return orig

    if is_NX(asset):
        original = find_original_for_NX(asset)
        original, NX = original, asset
    else:
        NX = find_NX_for_original(asset)
        original, NX = asset, NX

    return original, NX


def find_pairs(assets):
    """Accepts list of original assets OR list of NX assets OR mixed"""
    pairs = []
    for asset in assets:
        original_staticmesh, NX_staticmesh = find_original_and_NX(asset) 
        
        if not original_staticmesh or not NX_staticmesh:
            print(f'============SKipping for asset {asset}')
            continue

        pairs.append((original_staticmesh, NX_staticmesh))

    return pairs


def duplicate_NX_dir(assets_data: List) -> List[str]:
    '''Duplicate directory of static meshes with "_NX" suffix'''
    registry = unreal.AssetRegistryHelpers.get_asset_registry()
    
    duplicated = []
    for asset_path in assets_data:
        # original asset
        orig_asset_data = registry.get_asset_by_object_path(asset_path)

        number_of_assets = len(assets_data)
        text_label = f"Duplicating {number_of_assets} assets"
        with unreal.ScopedSlowTask(number_of_assets, text_label) as slow_task:
            slow_task.make_dialog(True)               # Makes the dialog visible, if it isn't already
            for i in range(number_of_assets):
                if slow_task.should_cancel():         # True if the user has pressed Cancel in the UI
                    break

                name = orig_asset_data.asset_name
                text_label = f"Duplicating {name}"
                slow_task.enter_progress_frame(1, desc=text_label)     # Advance progress by one frame.

                # duplication
                duplication_sucess, dupl_asset_path = duplicate_NX(orig_asset_data)
                if not duplication_sucess:
                    print(f'------------Skipping duplication {asset_path}')
                    continue
                duplicated.append(dupl_asset_path)

    return duplicated


def duplicate_NX(asset_data: unreal.AssetData):
    '''Duplicate static mesh with "_NX" suffix'''
    asset_name = str(asset_data.asset_name)
    asset_type = asset_data.asset_class
    
    duplication_sucess = False

    if '_NX' not in asset_name:
        source_asset_path = asset_data.package_name
        dest_asset_path = str(asset_data.package_name) + '_NX'
        loaded_duplicated_asset = unreal.EditorAssetLibrary.duplicate_asset(source_asset_path, dest_asset_path)

        if loaded_duplicated_asset:
            duplication_sucess = True
    else:
        # asset already duplicated
        dest_asset_path = str(asset_data.package_name) + '_NX'
        
    return (duplication_sucess, dest_asset_path)


def rename_NX():
    """Remove _NX suffix"""
    # nx_assets = get_assets_in_folder(path, NX=True, recursive=True)
    # assets = filter_by_class(assets, unreal.StaticMesh)
    
    nx_assets = unreal.EditorUtilityLibrary.get_selected_assets()
    for a in nx_assets:  
        print(type(a))  

        asset_name = a.get_name()    
        asset_folder = unreal.Paths.get_path(a.get_path_name())
        # Check if this asset is a Texture. Then check if it's name starts with T_. If not, prepend T_ to the name.
        
        if asset_name.startswith("Mesh"):
            new_asset_name = asset_name.lstrip('Mesh')
            asset_folder = unreal.Paths.get_path(a.get_path_name())

            unreal.log_error(f"Renaming {a.get_path_name()} to {asset_folder + new_asset_name}")
            unreal.EditorAssetLibrary.rename_asset(a.get_path_name(), asset_folder + new_asset_name)


rename_NX()