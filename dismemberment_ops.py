''''''
import unreal
import inspect
import os
import sys
from importlib import reload


thispath = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
if thispath not in sys.path:
    sys.path.append(thispath)

import SETTINGS
reload(SETTINGS)
from SETTINGS import DISM_LODS_SETTINGS
from utils_unreal import load_meshes, save_asset
from skeletal_mesh_lod_ops import set_lods, regenerate_lods


def test_lods():
    ASSET_PATH = "/Game/Disk/Char/Scorpion/Dism"
    loaded_assets = load_meshes(ASSET_PATH)
    loaded_skeletal_meshes = unreal.EditorFilterLibrary.by_class(loaded_assets, unreal.SkeletalMesh)

    print(f'==============Num of dismemberments {len(loaded_skeletal_meshes)}')

    for mesh in loaded_skeletal_meshes:
        # mesh_assets = unreal.EditorFilterLibrary.by_class(all_assets_loaded, class_)

        # set_lods(mesh, DISM_LODS_SETTINGS)
        lod_count = unreal.EditorSkeletalMeshLibrary.get_lod_count(mesh)
        if lod_count < 2:
            print(f"{mesh.get_name()} existing LOD count: {lod_count}")


def get_bone_removal_info(lod_infos: unreal.SkeletalMeshLODInfo):
    bones_to_remove_per_lod = []
    for lo in lod_infos:
        bones_to_remove = lo.get_editor_property('bones_to_remove')
        bones_to_remove_per_lod.append(bones_to_remove)
    
    return bones_to_remove_per_lod


def build_new_skeleton(self, skeleton, name, root):
    """
    COPY PASTED FROM GITHUB, DOES NOT WORK
    """
    new_skel = unreal.Skeleton(name)
    # add the root bone with -1 as parent
    new_skel.skeleton_add_bone(root, -1, FTransform())

    # copy bone indices from the original skeleton
    for index in range(0, skeleton.skeleton_bones_get_num()):
        # get bone name, parent index and ref pose
        bone_name = skeleton.skeleton_get_bone_name(index)
        bone_parent = skeleton.skeleton_get_parent_index(index)
        bone_transform = skeleton.skeleton_get_ref_bone_pose(index)

        # if this is the old 'root' bone (Hips), change its parent to the new 'root'
        if bone_parent == -1:
            bone_parent_name = root
        else:
            bone_parent_name = skeleton.skeleton_get_bone_name(bone_parent)

        # get new bone parent id
        new_bone_parent = new_skel.skeleton_find_bone_index(bone_parent_name)
        # add the new bone
        new_skel.skeleton_add_bone(bone_name, new_bone_parent, bone_transform)
    return new_skel


def transfer_bones_to_remove(source_skel_mesh, target_skel_mesh):
    source_lod_info = source_skel_mesh.get_editor_property('lod_info')
    target_lod_info = target_skel_mesh.get_editor_property('lod_info')

    bones_to_remove_per_lod = get_bone_removal_info(source_lod_info)

    if len(source_lod_info) != len(target_lod_info):
        # regenerate to match source lod count
        target_skel_mesh.regenerate_lod(new_lod_count=len(source_lod_info), regenerate_even_if_imported=True, generate_base_lod=True)
    
    for i, info in enumerate(target_lod_info):
        info.set_editor_property('bones_to_remove', bones_to_remove_per_lod[i])
        target_lod_info[i] = info


def transfer_reduction_settings(source_skel_mesh, target_skel_mesh):
    source_lod_info = source_skel_mesh.get_editor_property('lod_info')
    target_lod_info = target_skel_mesh.get_editor_property('lod_info')
    
    if len(source_lod_info) != len(target_lod_info):
        # regenerate to match source lod count
        print(f'transfer_reduction_settings REGEN LODS for {source_skel_mesh.get_name()}')
        target_skel_mesh.regenerate_lod(new_lod_count=len(source_lod_info), regenerate_even_if_imported=True, generate_base_lod=True)
    
    lod_infos = []
    for i, info in enumerate(target_lod_info):
            source_reduct_sett = source_lod_info[i].get_editor_property('reduction_settings')
            source_screensize = source_lod_info[i].get_editor_property('screen_size')

            info.set_editor_property('reduction_settings', source_reduct_sett)
            info.set_editor_property('screen_size', source_screensize)

            lod_infos.append(info)

    target_skel_mesh.set_editor_property('lod_info', lod_infos)


def generate_dism_lods(TARGET_ASSETS_PATH):
    """Generate Dismemberment lODs from predefined settings"""
    disms = load_meshes(TARGET_ASSETS_PATH)
    disms = unreal.EditorFilterLibrary.by_class(disms, unreal.SkeletalMesh)
    
    for dism in disms:
        set_lods(dism, DISM_LODS_SETTINGS)
        regenerate_lods(dism, lod_count=2)

        save_asset(dism)


def transfer_dism_lods(TARGET_ASSETS_PATH, SOURCE_PATH):
    """Transfers Dismemberment lOD settings from one char to another, i.e. Scorpion -> SubZero"""
    target_disms = load_meshes(TARGET_ASSETS_PATH)
    target_disms = unreal.EditorFilterLibrary.by_class(target_disms, unreal.SkeletalMesh)
    
    source_disms = load_meshes(SOURCE_PATH)
    source_disms = unreal.EditorFilterLibrary.by_class(source_disms, unreal.SkeletalMesh)

    for target in target_disms:

        source = find_source_dism(target, source_disms)
        if source:
            print(f'===========FOUND SOURCE for {target.get_name()} = {source.get_name()}')
            print(f'===========Transfering DISM for {target.get_name()}')
            transfer_bones_to_remove(source, target)
            transfer_reduction_settings(source, target)
        
            target.regenerate_lod(new_lod_count=len(source.get_editor_property('lod_info')))

        save_asset(target)



def parse_dism_name(mesh: unreal.SkeletalMesh):
    name = mesh.get_name()
    return '_'.join(name.split('_')[2:])


def find_source_dism(target, source_disms):
    target_name = parse_dism_name(target)

    for source in source_disms:
        source_name = parse_dism_name(source)

        if source_name == target_name:
            return source
    
    return None
  

# transfer_dism_lods()
SUBZERO_ASSET_PATH = "/Game/Disk/Char/SubZero/Dism"
SCORPION_ASSET_PATH = "/Game/Disk/Char/Scorpion/Dism"
transfer_dism_lods(SUBZERO_ASSET_PATH, SCORPION_ASSET_PATH)
