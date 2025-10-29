import unreal

# Define the new parent class
NEW_PARENT_CLASS = "/Script/Zirconium.ZrBasePhysActor"  # Change this to your desired class

# Define the folder where your Blueprints are stored
BP_FOLDER = "/Game/Prototype/Asset/Destruction/BasePhysObjects/"  # Change this to your actual Blueprint folder path

# Get the Asset Registry and retrieve all Blueprint assets in the specified folder
asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()
blueprint_assets = asset_registry.get_assets_by_path(BP_FOLDER, recursive=True)

# Load the new C++ parent class once
new_parent = unreal.load_object(None, NEW_PARENT_CLASS)
if new_parent is None:
    print(f"Error: Could not load the new parent class {NEW_PARENT_CLASS}")
else:
    # Iterate over each asset and update the parent class if it's a Blueprint
    for asset_data in blueprint_assets:
        blueprint = asset_data.get_asset()
        if isinstance(blueprint, unreal.Blueprint):
            # Retrieve the old parent class via the Blueprint's generated class
            generated_class = blueprint.generated_class()
            if generated_class:
                # Use the generated class's super class as the old parent
                old_parent = generated_class.get_super_class()
                old_parent_path = old_parent.get_path_name() if old_parent else "None"
            else:
                old_parent_path = "Unknown (not compiled?)"
                
            print(f"Changing Parent for: {blueprint.get_name()} (Old: {old_parent_path})")

            # Set the new parent class using the editor property setter
            blueprint.set_editor_property("ParentClass", new_parent)

            # Optionally compile the Blueprint after reparenting
            unreal.KismetEditorUtilities.compile_blueprint(blueprint)

            # Save the updated Blueprint
            editor_util.save_loaded_asset(blueprint)
            print(f"Updated: {blueprint.get_name()} → New Parent: {NEW_PARENT_CLASS}")

    print("Batch Parent Class Change Complete!")