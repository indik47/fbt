import unreal


# animation_sequence = '/Game/Disk/Env/TeaHouse/Anim/CH01_ALL_FJF04_FJM20_FJM21_001_Emily.CH01_ALL_FJF04_FJM20_FJM21_001_Emily'
animation_sequence = '/Game/Disk/Env/TeaHouse/Anim/CH01_ALL_FJF04_FJM20_FJM21_001_Sean.CH01_ALL_FJF04_FJM20_FJM21_001_Sean'
# sm = '/Game/Disk/Env/TeaHouse/Asset/TeaHouse_LargePosters/Mesh/SM_TeaHouse_LargePoster_2.SM_TeaHouse_LargePoster_2'

loaded = unreal.load_asset(animation_sequence)

# unreal.log(loaded)
# unreal.log(unreal.AnimationLibrary.get_sequence_length(loaded))
# AnimCurveCompressionSettings = unreal.AnimationLibrary.get_curve_compression_settings(loaded)
unreal.AnimationLibrary.finalize_bone_animation(loaded)
# unreal.log(AnimCurveCompressionSettings)
# unreal.log(AnimCurveCompressionSettings.get_editor_property('codec'))


# def get_asset_editor() -> unreal.AssetEditorSubsystem:
    # return unreal.get_editor_subsystem(unreal.AssetEditorSubsystem)
# 
# ae_sub = get_asset_editor()

# for _ in sorted(dir(unreal.get_editor_subsystem())):
#     print(_)

# sm_editor = unreal.StaticMeshEditor()
# print(sm_editor)


