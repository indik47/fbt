import unreal
import traceback


def filter_def_lit(mat):
    '''Filter materials that have DEFAULT_LIT shading model'''
    shading_model = mat.get_editor_property('shading_model')

    return shading_model == unreal.MaterialShadingModel.MSM_DEFAULT_LIT


def filter_mats(mats):
    # filter those that have default_lit shading model
    mats_to_exclude = list(filter(filter_def_lit, mats))
    if mats_to_exclude:
        mats_to_modify = [x for x in mats if x not in mats_to_exclude]
    else:
        mats_to_modify = mats
    
    return mats_to_modify, mats_to_exclude


def print_summary(mats_to_modify, mats_to_exclude):
    unreal.log(f'Modified {len(mats_to_modify)} mats')
    if mats_to_exclude:
        unreal.log(f'{len(mats_to_exclude)} mats already had DEFAULT_LIT shading model')


def change_shading_model(mat:unreal.Material, shading_model:unreal.MaterialShadingModel):
        try:
            mat.set_editor_property('shading_model', shading_model)
        except:
            traceback.print_exc()


def main():
    selected_assets = unreal.EditorUtilityLibrary.get_selected_assets()
    mats = list(filter(lambda a:type(a) == unreal.Material, selected_assets))

    mats_to_modify, mats_to_exclude = filter_mats(mats)

    for mat in mats_to_modify:
        unreal.log_warning(f'Setting shading model to DEFAULT_LIT for {mat.get_name()}')
        change_shading_model(mat, unreal.MaterialShadingModel.MSM_DEFAULT_LIT)

    print_summary(mats_to_modify, mats_to_exclude)


main()