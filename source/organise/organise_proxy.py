import unreal
from importlib import reload


import fbyte.source.utils.utils_material as utils_material
import fbyte.source.utils.utils_general as utils_general
from fbyte.source.mat.replace_mats import PathOps
reload(utils_material)
reload(utils_general)


def prepare_proxy_dirs(asset_dir):
    smesh_dir = asset_dir + '/Mesh'
    mtl_dir = asset_dir + '/Mat'
    tex_dir = asset_dir + '/Texture'
    utils_general.prepare_dir(smesh_dir)
    utils_general.prepare_dir(mtl_dir)
    utils_general.prepare_dir(tex_dir)

    return smesh_dir, mtl_dir, tex_dir


def filter_selection(selection):
    """Filter selection in PROXY subdir. After PROXY creation there should be 1 staticmesh, 1 material and 2 textures."""

    asset_name, asset_dir = utils_general.parse_(selection[0])
    named_asset_dir = PathOps.named_asset_folder(asset_dir)

    smeshes = utils_general.filter_by_class(selection, unreal.StaticMesh)


    textures = utils_general.filter_by_class(selection, unreal.Texture2D)
    source_minstances = utils_general.filter_by_class(selection, unreal.MaterialInstanceConstant)

    return smeshes, source_minstances, textures


def check_PROXY_meshes(smeshes):   
    if len(smeshes) != 1:
        unreal.log_warning(f"More than 1 mesh in selection, skipping...")
        return

    proxy_sm_asset = smeshes[0]

    return proxy_sm_asset


def check_PROXY_mi(source_minstances):
    if len(source_minstances) != 1:
        unreal.log_warning(f"Only 1 material should be in selected PROXY assets, skipping...")
        return
    source_mi = source_minstances[0]

    return source_mi


def check_PROXY_textures(textures):
    if len(textures) != 2:
        unreal.log_warning(f"Only Diffuse and Normal textures should be in PROXY subdir, skipping...")
        return

    return textures


def rename_textures(diff, normal, tex_dir):
    diff_source = diff.get_path_name()
    diff_target = tex_dir + '/' + diff.get_name().replace('_Diffuse', '_D')

    normal_source = normal.get_path_name()
    normal_target = tex_dir + '/' + normal.get_name().replace('_Normal', '_N')

    unreal.EditorAssetLibrary.rename_asset(diff_source, diff_target)
    unreal.EditorAssetLibrary.rename_asset(normal_source, normal_target)

    return diff_target, normal_target


def rename_mesh(sm_asset, smesh_dir):
    mesh_source_name = sm_asset.get_path_name()
    mesh_target_name = smesh_dir + '/' + sm_asset.get_name()
    unreal.EditorAssetLibrary.rename_asset(mesh_source_name, mesh_target_name)


def create_proxy_mat_instance(source_mi, mtl_dir, diff):
    target_mi_name = source_mi.get_name()
    target_mi_name = target_mi_name.replace('M_', 'MI_')

    # create material instance
    parent_mtl = unreal.EditorAssetLibrary.find_asset_data('/Game/Disk/Saber/Shared/Libs/Mat/Env/BaseMat/M_Env_StaticOpaque_FullyRough.M_Env_StaticOpaque_FullyRough')
    target_mi = utils_material.create_mtl_instance(parent_mtl, target_mi_name, mtl_dir, diff)
    
    # save mi
    saved = unreal.EditorAssetLibrary.save_asset(target_mi.get_path_name())
    unreal.log_warning(f"Saved MI: {saved}")

    return target_mi


def organize_proxy():
    sm_assets, mat_instances, textures = filter_selection(unreal.EditorUtilityLibrary.get_selected_assets())
    sm_asset = check_PROXY_meshes(sm_assets)
    source_mi = check_PROXY_mi(mat_instances)
    textures = check_PROXY_textures(textures)

    proxy_asset_name, proxy_dir = utils_general.parse_(sm_asset)
    classified = utils_material.classify_textures(textures)

    try:
        diff, normal = classified['diffuse'][0], classified['normal'][0]
    except KeyError:
        unreal.log_warning(f"Diffuse or Normal texture not found in PROXY subdir, skipping...")
        return

    smesh_dir, mtl_dir, tex_dir = prepare_proxy_dirs(proxy_dir)
    
    # create mi and assign material instance to mesh
    target_mi = create_proxy_mat_instance(source_mi, mtl_dir, diff)
    unreal.log_warning(f"-----Assigning MI: {target_mi.get_path_name()} to {sm_asset.get_name()}")
    unreal.log_warning(f"-----SM fullname = {sm_asset.get_path_name()}")
    sm_asset.set_material(0, target_mi)
        
    rename_textures(diff, normal, tex_dir)
    rename_mesh(sm_asset, smesh_dir)

    unreal.log_warning(f'Deleting source MI: {source_mi.get_path_name()}')
    unreal.EditorAssetLibrary.delete_asset(source_mi.get_path_name())


organize_proxy()

