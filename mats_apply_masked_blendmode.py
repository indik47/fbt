"""Change blend model of materials to MASKED

How to use:
1. Select materials in Content Browser (any number of materials)
2. Run this script (File -> Run Python Script...)
3. Check the log for results (Window -> Developer Tools -> Output Log)
4. Save modified materials
"""
import unreal
import traceback


def filter_blendmode_masked(mat):
    '''Filter materials that have BLEND_MASKED blend mode'''
    blend_mode = mat.get_editor_property('blend_mode')

    return blend_mode == unreal.BlendMode.BLEND_MASKED


def filter_blendmode_translucent(mat):
    '''Filter materials that have BLEND_MASKED blend mode'''
    blend_mode = mat.get_editor_property('blend_mode')

    return blend_mode == unreal.BlendMode.BLEND_TRANSLUCENT


def filter_mats(mats):
    '''filter mats which have non-masked blend mode'''
    mats_to_exclude_masked = list(filter(filter_blendmode_masked, mats))
    mats_to_exclude_transl = list(filter(filter_blendmode_translucent, mats))


    if mats_to_exclude_masked:
        mats_to_modify = [x for x in mats if x not in mats_to_exclude_masked]
    else:
        mats_to_modify = mats
    
    if mats_to_exclude_transl:
        mats_to_modify = [x for x in mats_to_modify if x not in mats_to_exclude_transl]
    else:
        mats_to_modify = mats_to_modify

    mats_to_exclude = mats_to_exclude_masked + mats_to_exclude_transl
    
    return mats_to_modify, mats_to_exclude


def print_summary(mats_to_modify, mats_to_exclude):
    unreal.log_warning(f'Modified {len(mats_to_modify)} mats')
    if mats_to_exclude:
        unreal.log_warning(f'{len(mats_to_exclude)} mats were NOT modified')


def change_blendmode(mat:unreal.Material, blend_mode:unreal.BlendMode):
        try:
            mat.set_editor_property('blend_mode', blend_mode)
        except:
            traceback.print_exc()


def main():
    selected_assets = unreal.EditorUtilityLibrary.get_selected_assets()
    mats = list(filter(lambda a:type(a) == unreal.Material, selected_assets))

    mats_to_modify, mats_to_exclude = filter_mats(mats)

    for mat in mats_to_modify:
        unreal.log_warning(f'Setting MASKED blend mode for {mat.get_name()}')
        change_blendmode(mat, unreal.BlendMode.BLEND_MASKED)

    print_summary(mats_to_modify, mats_to_exclude)


main()