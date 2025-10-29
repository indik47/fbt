import unreal

def get_asset_creation_time(asset_path):
    # Get the AssetRegistryModule
    asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()

    # Get the AssetData for the specified asset
    asset_data = asset_registry.get_asset_by_object_path(asset_path)

    if asset_data.is_valid():
        # Get the creation time from the AssetData
        creation_time = asset_data.get_meta_data("FileCreateDate")
        return creation_time

    return None

# Example usage
asset_name = '/Game/Disk/MapMode/Env/NPC_Props/BowlAndMixer/FireTemple_BowlAndMixer.FireTemple_BowlAndMixer'
loaded_asset = unreal.EditorAssetLibrary.load_asset(asset_name)
all_metadata = unreal.EditorAssetLibrary.get_metadata_tag_values(loaded_asset)
unreal.log(all_metadata)
# for tag_name, value in all_metadata.iteritems():
    # if not value is "":
        # unreal.log("Value of tag " + str(tag_name) + " for asset " + asset_name + ": " + value)