import unreal

def rename_NX():
    """Remove _NX suffix for selected assets"""  
    selected = unreal.EditorUtilityLibrary.get_selected_assets()
    unreal.log("Selected assets: {0}".format(selected))
               
    for asset in selected:  
        asset_name = asset.get_name()  
        unreal.log_warning(f"Asset name: {asset_name}")  
        asset_folder = unreal.Paths.get_path(asset.get_path_name())
        unreal.log_warning(f"Asset folder: {asset_folder}")

        new_asset_name = asset_name.rstrip('_NX')

        unreal.log_warning(f"Renaming {asset.get_path_name()} to {asset_folder + new_asset_name}")
        unreal.EditorAssetLibrary.rename_asset(asset.get_path_name(), asset_folder + '/' + new_asset_name)


rename_NX()