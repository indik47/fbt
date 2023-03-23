import sys
import unreal
from importlib import reload

thispath = r'C:\Projects\k1\Content\Code'
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


def get_dependencies(asset_path):
    """Experimental"""
    reg = unreal.AssetRegistryHelpers.get_asset_registry()

    asset_data = reg.get_asset_by_object_path(asset_path)
    opt = unreal.AssetReAssetRegistryDependencyOptions(include_soft_package_references=True, include_hard_package_references=True, include_searchable_names=False, include_soft_management_references=False, include_hard_management_references=False)
    dep = reg.get_dependencies(asset_data.package_name, opt)

    print(dep)


def replace_NX():
    sel_actors = unreal.EditorLevelLibrary.get_selected_level_actors()
    gu = unreal.ActorGroupingUtils.get()
    gu.unlock_selected_groups()
    # gu.ungroup_actors(sel_actors)

    for actor in sel_actors:
        print(f'================REPLACING ACTOR = {actor}')
        pairs = duplicate_ops.find_pairs([actor.root_component.static_mesh.get_path_name()])
        orig_statimesh, NX_replacement_staticmesh = pairs[0]
        print(orig_statimesh, NX_replacement_staticmesh)

        if NX_replacement_staticmesh:
            sm = unreal.load_asset(NX_replacement_staticmesh)
            actor.root_component.set_editor_property('static_mesh', sm)
            
            # full actor replacement (different object)
            # unreal.EditorLevelLibrary.set_selected_level_actors([actor])
            # unreal.EditorLevelLibrary.replace_selected_actors(NX_replacement_staticmesh)

        unreal.EditorLevelLibrary.set_selected_level_actors(sel_actors)
        gu.lock_selected_groups()

replace_NX()
