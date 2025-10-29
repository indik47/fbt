import json
import unreal


def save_json(data, path, name):
    with open(path + r"\\" + name, 'w+') as fhandle:
        json.dump(data, fhandle, indent=2)


def save_asset(asset) -> bool:
    return unreal.EditorAssetLibrary.save_loaded_asset(asset)


def load_meshes(asset_path):
    all_assets = unreal.EditorAssetLibrary.list_assets(asset_path, recursive=True)
    
    # load into memory
    all_assets_loaded = [unreal.EditorAssetLibrary.load_asset(a) for a in all_assets]

    return all_assets_loaded


def get_selected_assets():
    selected  = unreal.EditorUtilityLibrary.get_selected_assets()
    return selected



