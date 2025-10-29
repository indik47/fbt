import unreal


def delete_NX_dir(assets_dir: str):
    """Delete _NX meshes from assets dir"""
    
    assets = unreal.EditorAssetLibrary.list_assets(assets_dir, recursive=False)
    NX_assets = list(filter(lambda asset:'_NX' in asset, assets))

    deleted = []
    for asset_path in NX_assets:
        # unreal.EditorAssetLibrary.delete_asset(asset_path)
        deleted.append(asset_path)
    
    return deleted