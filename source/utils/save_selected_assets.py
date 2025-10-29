import unreal

selected = unreal.EditorUtilityLibrary.get_selected_assets()

if selected:
    number_of_assets = len(selected)

    for asset in selected:
        asset_name = asset.get_name()
        text_label = f"Saving {number_of_assets} assets"

        with unreal.ScopedSlowTask(number_of_assets, text_label) as slow_task:
            slow_task.make_dialog(True)               # Makes the dialog visible, if it isn't already
            if slow_task.should_cancel():         # True if the user has pressed Cancel in the UI
                break

            text_label = f"Saving {asset_name}"
            slow_task.enter_progress_frame(1, desc=text_label)     # Advance progress by one frame.

            print(f'===============Saving {asset.get_name()}')
            unreal.EditorAssetLibrary.save_loaded_asset(asset, only_if_is_dirty=False)
