import unreal
import inspect
import os
import sys
from importlib import reload

thispath = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
if thispath not in sys.path:
    sys.path.append(thispath)


from utils_unreal import load_meshes, save_asset
import duplicate_ops
from SETTINGS import DISM_LODS_SETTINGS

reload(duplicate_ops)



def validate_lod_data(data) -> bool:
    #TODO write validation
    # check if the mesh is complex enough.
    # number_of_vertices = unreal.EditorSkeletalMeshLibrary.get_num_verts(skeletal_mesh, 0)
    # if number_of_vertices < 10:
    #     return
    return True


def prepare_lod_info(data):
    opt_settings = unreal.SkeletalMeshOptimizationSettings()
    # default reduction settings
    opt_settings.set_editor_property('termination_criterion', unreal.SkeletalMeshTerminationCriterion.SMTC_NUM_OF_VERTS)
    # percentage = 1.0 for it not to interfere with max_num
    opt_settings.set_editor_property('num_of_vert_percentage', 1.0)

    # passed in settings
    opt_settings.set_editor_property('base_lod', data['base_lod'])
    opt_settings.set_editor_property('max_num_of_verts_percentage', data['number_of_verts'])

    lod_info = unreal.SkeletalMeshLODInfo()
    lod_info.set_editor_property('reduction_settings', opt_settings)

    scr_size = unreal.PerPlatformFloat()
    scr_size.set_editor_property('default', data['screen_size'])
    lod_info.set_editor_property('screen_size', scr_size)
    
    return lod_info


def set_lods(skel_mesh: unreal.SkeletalMesh, lods_data, debug=False) -> None:
    if debug:
        print("treating asset: " + skel_mesh.get_name())
        print("existing LOD count: " + str(unreal.EditorSkeletalMeshLibrary.get_lod_count(skel_mesh)))

    lod_data_valid = validate_lod_data(lods_data)
    if not lod_data_valid:
        print(f'ERROR LOD data for {skel_mesh} is not valid')
        return

    lod_info = [prepare_lod_info(data) for data in lods_data]
    skel_mesh.set_editor_property('lod_info', lod_info)



def regenerate_lods(skel_mesh: unreal.SkeletalMesh, lod_count=1) -> bool:
    success = skel_mesh.regenerate_lod(new_lod_count=lod_count, regenerate_even_if_imported=True, generate_base_lod=True)
    if success:
        print(f'Regenerated LoDs for {skel_mesh}')
    else:
        print(f'FAILED to Regenerated LoDs for {skel_mesh}')
    
    return success


