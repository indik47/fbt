import unreal

# Get selected assets in Content Browser
selected_assets = unreal.EditorUtilityLibrary.get_selected_assets()

if not selected_assets:
    unreal.log_warning("No assets selected!")
else:
    asset_paths = [asset.get_path_name() for asset in selected_assets]

    # File paths
    save_dir = unreal.Paths.project_saved_dir()
    save_dir = "C:\\Projects\\ZR\\"
    #output_path = save_dir + "selected_assets.txt"
    output_path = save_dir +"selected_phys_assets.txt"


    # Save asset paths to file
    with open(output_path, 'w') as file:
        for path in asset_paths:
            file.write(f"{path}\n")

    unreal.log(f"Selected asset paths saved to: {output_path}")

    # Save asset thumbnails
    thumbnail_tools = unreal.AssetThumbnailTools()

    # Filter out assets that are not physics assets with the parent class ZrBasePhysObject
    filtered_assets = []
    for asset in selected_assets:
        asset_class = asset.get_class()
        parent_class = unreal.EditorAssetLibrary.get_parent_class(asset_class)
        if parent_class and parent_class.get_name() == "ZrBasePhysObject":
            filtered_assets.append(asset)

    selected_assets = filtered_assets
    
    
    

    
    
    for asset in selected_assets:
        thumbnail = thumbnail_tools.capture_thumbnail(asset, 256, 256)
        asset_name = asset.get_name()
        thumbnail_path = f"{save_dir}{asset_name}_thumbnail.png"

        if thumbnail_tools.export_thumbnail(thumbnail, thumbnail_path):
            unreal.log(f"Thumbnail saved for asset {asset_name} at: {thumbnail_path}")
        else:
            unreal.log_warning(f"Failed to save thumbnail for asset {asset_name}")