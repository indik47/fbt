import sys
import os
import inspect
import unreal
from typing import List
from importlib import reload

thispath = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
if thispath not in sys.path:
    sys.path.append(thispath)


import SETTINGS
import duplicate_ops
import cleanup_ops
import static_mesh_lod_ops

reload(SETTINGS)
reload(duplicate_ops)
reload(cleanup_ops)
reload(static_mesh_lod_ops)


def has_lods(mesh:unreal.StaticMesh):
    num_lods = unreal.EditorStaticMeshLibrary.get_lod_count(mesh)
    if num_lods > 1:
        return True
    
    return False


def apply_default_LODs(NX_staticmesh: unreal.StaticMesh, skipLOD0=True):
        static_mesh_lod_ops.generate_lods(NX_staticmesh, SETTINGS.DEFAULT_LODs_SCREEN_SIZES)

        if skipLOD0:
            startLOD = 1
        else:
            startLOD = 0

        endLOD = NX_staticmesh.get_num_lods()

        static_mesh_lod_ops.apply_def_lods_settings(startLOD, endLOD, NX_staticmesh, SETTINGS.DEFAULT_LODs_SETTINGS)
        return NX_staticmesh


def transfer_lods(source_loaded: unreal.StaticMesh, NX_staticmesh: unreal.StaticMesh):
    """Transfer lods from Source to NX"""
    screen_sizes = unreal.EditorStaticMeshLibrary.get_lod_screen_sizes(source_loaded)
    reduction_settings = static_mesh_lod_ops.get_lods_settings(source_loaded)

    static_mesh_lod_ops.generate_lods(NX_staticmesh, screen_sizes)
    static_mesh_lod_ops.apply_lods_settings(reduction_settings, NX_staticmesh)


def set_lods(folders:List, skip_existing_NX=False):
    for folder in folders:
        # duplicate
        all_assets = duplicate_ops.get_assets_in_folder(path=folder)
        static_meshes = duplicate_ops.filter_by_class(all_assets, unreal.StaticMesh)
        duplicated = duplicate_ops.duplicate_NX_dir(static_meshes)
        
        if skip_existing_NX:
            # do LODs only for new duplicates
            processed_assets = duplicate_ops.find_pairs(duplicated)
        else:
            # do LODs for all assets in folder (including those that had NX duplicates previously)
            processed_assets = duplicate_ops.find_pairs(all_assets)

        # apply lods
        processed_NX_assets = []
        for (source, NX) in processed_assets:
            source_loaded = unreal.load_asset(source)
            NX_loaded = unreal.load_asset(NX)

            if has_lods(source_loaded):
                transfer_lods(source_loaded, NX_loaded)
            else:   
                apply_default_LODs(NX_loaded)
            
            processed_NX_assets.append(NX_loaded)

        unreal.EditorAssetLibrary.save_loaded_assets(processed_NX_assets)


set_lods(SETTINGS.TeaHouse_folders)


# def remake_lods (folders:List):
#     for folder in folders:
#         NX_assets_in_folder = duplicate_ops.get_assets_in_folder(path=folder, NX=True)
#         NX_data = get_NX_lods_data()

        

# TODO write functionality:
# DONE 1) duplicate and FORCE lod data copy to all NX (all folder)
# prepare_lods(SETTINGS.TeaHouse_dirs, skip_existing_NX=False)

# DONE 2) duplicate and copy LOD data only to newly duplicated
# prepare_lods(SETTINGS.TeaHouse_dirs, skip_existing_NX=True)

# 3) save NXdata, delete NX, duplicate and copy lod data only to newly duplicated



