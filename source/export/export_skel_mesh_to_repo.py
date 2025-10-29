import unreal
import re
import os
from typing import List


# helper method to get all actors IN LEVEL
def get_actors(use_selection = False, actor_class = None, actor_tag = None) -> List[unreal.Actor]:
    if use_selection:
        selected_actors = unreal.EditorLevelLibrary.get_selected_level_actors()
        class_actors = selected_actors
        if actor_class:
            class_actors = [x for x in selected_actors if cast(x,actor_class)]
        tag_actors = class_actors
        if actor_tag:
            tag_actors = [x for x in selected_actors if x.actor_has_tag(actor_tag)]
        return [x for x in tag_actors]

    elif actor_class:
        actors = unreal.GameplayStatics.get_all_actors_of_class(unreal.EditorLevelLibrary.get_editor_world(), actor_class)
        tag_actors = actors
        if actor_tag:
            tag_actors = [x for x in actors if x.actor_has_tag(actor_tag)]
        return [x for x in tag_actors]

    elif actor_tag:
        tag_actors = unreal.GameplayStatics.get_all_actors_of_class(unreal.EditorLevelLibrary.get_editor_world(),actor_tag)
        return [x for x in tag_actors]

    else:
        actors = unreal.GameplayStatics.get_all_actors_of_class(unreal.EditorLevelLibrary.get_editor_world(),unreal.Actor)

        return [x for x in actors]

# helper method to get all actors IN CONTENT BROWSER
def get_assets(use_selection=False, asset_class=None) -> List:
    if use_selection:
        assets_data = unreal.EditorUtilityLibrary.get_selected_asset_data()
        return assets_data

    if asset_class:
        assets_data = unreal.AssetRegistryHelpers.get_asset_registry().get_assets_by_class(asset_class)
    else:
        assets_data = unreal.AssetRegistryHelpers.get_asset_registry().get_all_assets()
    
    return assets_data


#A helper method to find actor matching given name
def get_actors_by_name(actors, name):
    r = re.compile(name + '*')
    result = [x for x in actors if r.match(x.get_name())]
    return [x for x in result]


def export_fbx(filepath):
    #TODO implement
    """Not working (could probably works on selected ACTORS)"""
    selected_actors = unreal.EditorLevelLibrary.get_selected_level_actors()
    if len(selected_actors) == 0:
        print("No actor selected, nothing to export")
        quit()

    for actor in selected_actors:
        print(actor)
        task = unreal.AssetExportTask()
        task.object = actor #selected_actors[0].get_world()
        task.filename = filepath + '/' + actor.get_name()  + ".fbx"
        task.selected = True
        task.replace_identical = False
        task.prompt = False
        task.automated = True
        
        task.options = unreal.FbxExportOption()
        task.options.vertex_color = False
        task.options.collision = False
        task.options.level_of_detail = False

        unreal.Exporter.run_asset_export_task(task)


def export_fbx3(destination_path, asset):
    # WORKING
    # selected assets in Content Browser
    system_lib = unreal.SystemLibrary()
    
    # Setup AssetExportTask for non-interactive mode
    task = unreal.AssetExportTask()
    task.object = asset      # the asset to export
    task.filename = os.path.join(destination_path, asset.get_name() + ".fbx")       # the filename to export as
    task.automated = True           # don't display the export options dialog
    task.replace_identical = True   # always overwrite the output

    # Setup export options for the export task
    task.options = unreal.FbxExportOption()
    # These are the default options for the FBX export
    # task.options.fbx_export_compatibility = fbx_2013
    # task.options.ascii = False
    # task.options.force_front_x_axis = False
    # task.options.vertex_color = True
    # task.options.level_of_detail = True
    # task.options.collision = True
    # task.options.welded_vertices = True
    # task.options.map_skeletal_motion_to_root = False

    unreal.Exporter.run_asset_export_task(task)


def export_texture2d(destination_path, asset):
    # WORKING
    # selected assets in Content Browser
    system_lib = unreal.SystemLibrary()
    
    # Setup AssetExportTask for non-interactive mode
    task = unreal.AssetExportTask()
    task.object = asset      # the asset to export
    task.filename = os.path.join(destination_path, asset.get_name() + ".tga")       # the filename to export as
    task.automated = True           # don't display the export options dialog
    task.replace_identical = True   # always overwrite the output

    # Setup export options for the export task
    # task.options = unreal.FbxExportOption()
    # These are the default options for the FBX export
    # task.options.fbx_export_compatibility = fbx_2013
    # task.options.ascii = False
    # task.options.force_front_x_axis = False
    # task.options.vertex_color = True
    # task.options.level_of_detail = True
    # task.options.collision = True
    # task.options.welded_vertices = True
    # task.options.map_skeletal_motion_to_root = False

    unreal.Exporter.run_asset_export_task(task)


def get_static_mesh_mat(static_mesh: unreal.StaticMesh):
    if static_mesh is None:
        return

    material_instances = []

    # iterate on all material slots
    for material_index in range(0, static_mesh.get_num_sections(0)):
        material = static_mesh.get_material(material_index)
        if isinstance(material, unreal.MaterialInstance):
            material_instances.append(material)

    return material_instances
        

def get_skeletal_mesh_mats(skeletal_mesh: unreal.SkeletalMesh):
    material_instances = []
    materials = skeletal_mesh.materials

    for material in materials:
        mat_interface = material.material_interface

        if isinstance(mat_interface, unreal.MaterialInstance):
            material_instances.append(mat_interface)
    
    return material_instances


def get_skeletal_mesh_actor_mat(actor: unreal.SkeletalMeshActor):
    """Get mat instances from SkeletalMeshActor"""
    mat_instances = []
    mats = actor.skeletal_mesh_component.get_materials()
    for mat in mats:
        if isinstance(mat, unreal.MaterialInstance):
            mat_instances.append(mat)
    
    return mat_instances


def get_textures(material: unreal.MaterialInstance):
    """Get textures for MaterialInstance"""
    textures = []
    textures_params = material.texture_parameter_values

    for t in textures_params:
        texture = t.parameter_value
        if texture not in textures:
            textures.append(texture)

    return textures


def work_with_actors():
    def filter_cb(actor):
        for wanted_name in wanted:
            if actor.get_name() in wanted_name:
                return True
        
        return False

    wanted = ['SK_Mannequin']
    actors = get_actors(actor_class=unreal.SkeletalMeshActor)
    actors = list(filter(filter_cb, actors))
    print(actors)

    for actor in actors:
        mat_instances = get_skeletal_mesh_actor_mat(actor)
        for mat_instance in mat_instances:
            textures = get_textures(mat_instance)
            print(textures)


def get_asset_registry() -> unreal.AssetRegistry:
    return unreal.AssetRegistryHelpers.get_asset_registry()


def prepare_data():
    data = {
        'Scorpion': {'assets': ['SK_Scorpion_Skin001_A', 'SK_Scorpion_Skin002_A', 'SK_Scorpion_Skin003_A']},
        'Havik': {'assets': ['SK_Havik_Skin004_A']},
    }
    # data = {'Scorpion': {'assets': ['SK_Scorpion_Skin001_A']}}
    return data


def work_with_asset_registry():
    registry = get_asset_registry()
    # DEPENDENCIES
    # options = unreal.AssetRegistryDependencyOptions(include_soft_package_references=True, include_hard_package_references=True, include_searchable_names=True, include_soft_management_references=True, include_hard_management_references=True)
    # print(registry.get_dependencies(path+asset, options))


def work_with_assets():
    """Tmp func"""

    export_path_top = r'C:\Projects\k1\Content\Retopology\Char\Scorpion_Skin001A\Scorpion SOURCE\Texture'

    data = prepare_data()
    char = 'Havik'
    scorpion_assets = data[char]['assets']

    assets_data = get_assets()
    filtered = list(filter(lambda asset: asset.asset_name in scorpion_assets, assets_data))
    
    for asset_data in filtered:
        export_path = os.path.join(export_path_top, char)

        if not os.path.exists(export_path):
            os.mkdir(export_path)

        asset = unreal.load_asset(asset_data.object_path)

        if isinstance(asset, unreal.SkeletalMesh):
            print(f'Exporting skeletal mesh {asset.get_name()}')
            export_skeletal_mesh_textures(export_path, asset)

        elif isinstance(asset, unreal.StaticMesh):
            print(f'Exporting static mesh {asset.get_name()}')
            mats = get_static_mesh_mat(asset)

            #TODO export textures for static meshes

        export_fbx3(export_path, asset)

def export_skeletal_mesh_textures(export_path, asset):
    mats = get_skeletal_mesh_mats(asset)

    for mat in mats:
        textures = get_textures(mat)
        for t in textures:
            export_texture2d(export_path, t)



# work_with_actors()
# work_with_assets()

skeletal_mesh = '/Game/Disk/Char/Scorpion/Skin/001/Mesh/SK_Scorpion_Skin001_A.SK_Scorpion_Skin001_A'
export_path = r'C:\Projects\k1\Content\Retopology\Char\Scorpion_Skin001A\Scorpion SOURCE\Texture'

export_skeletal_mesh_textures(export_path, unreal.load_asset(skeletal_mesh))