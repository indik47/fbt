import os
import traceback
import unreal
import sys 
import re

def get_material_slot_names(static_mesh):
    """https://forums.unrealengine.com/t/get-material-slot-names-for-static-mesh-in-python/468590/2
    Ok, so the function get_material_slot_names() is a method of the StaticMeshComponent class. 
    So you are able to retrieve the materials from base StaticMesh class by first creating a StaticMeshComponent, setting your asset as the static mesh property, 
    then calling get_material_slot_names()"""

    sm_component = unreal.StaticMeshComponent()
    sm_component.set_static_mesh(static_mesh)
    return unreal.StaticMeshComponent.get_materials(sm_component)



def create_mtl_instance(base_mtl, mi_name, mi_folder, diff_texture):
    AssetTools = unreal.AssetToolsHelpers.get_asset_tools()
    mi_asset = AssetTools.create_asset(mi_name, mi_folder, unreal.MaterialInstanceConstant, unreal.MaterialInstanceConstantFactoryNew())        
        
    # set material instance parameters!
    unreal.MaterialEditingLibrary.set_material_instance_parent( mi_asset, base_mtl.get_asset() )  # set parent material
    unreal.MaterialEditingLibrary.set_material_instance_texture_parameter_value( mi_asset, "Color", diff_texture ) # set scalar parameter 

    return mi_asset


#TODO refactor
"""Copied from export_skel_mesh_to_repo.py"""
def get_textures(material: unreal.MaterialInstance):
    """Get textures for MaterialInstance"""
    textures = []
    textures_params = material.texture_parameter_values

    for t in textures_params:
        texture = t.parameter_value
        if texture not in textures:
            textures.append(texture)

    return textures


#TODO refactor
"""Copied from export_skel_mesh_to_repo.py"""
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


def main():
    destination_path = 'C:\Projects\k1'
    asset_ref = '/Game/Disk/Env/TeaHouse/Asset/TeaHouse_Railing/Mesh/SM_TeaHouse_Railing_4.SM_TeaHouse_Railing_4'
    sm = unreal.load_asset(asset_ref)

    mats = get_material_slot_names(sm)
    for mat in mats:
        print(mat)
        
        for tex in get_textures(mat):
            print(tex)
            # export_texture2d(destination_path, tex)


def classify_textures(textures):
    """Classify textures by type"""
    classified = {
        'diffuse': [],
        'normal': [],
        'other': []

    }

    for tex in textures:
        if re.findall(r'_d|diffuse|dDiff', tex.get_name(), re.IGNORECASE):
            classified['diffuse'].append(tex)
        elif re.findall(r'_n|normal|nrm', tex.get_name(), re.IGNORECASE):
            classified['normal'].append(tex)

        else:
            classified['other'].append(tex)

    return classified


if __name__=='__main__':
    main()