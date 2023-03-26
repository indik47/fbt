import os
import sys
from typing import Union
import unreal
import inspect
from importlib import reload
from enum import Enum
import re


thispath = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
if thispath not in sys.path:
    sys.path.append(thispath)

import source.mat.material_ops as material_ops
reload(material_ops)


class AssetType(Enum):
    UNKNOWN = 0
    NRS_REGULAR_ASSET = 1
    SABER_MERGED = 2
    SABER_PROXY = 3
    SABER_BAKED = 4
    SABER_ENV = 5
    SABER_CHAR = 6
    NRS_MATERIAL = 7


def classify_asset(asset:unreal.StaticMesh):
    """Classify asset by name"""
    asset_name, asset_folder = parse_(asset)

    # regex that checks if asset_folder contains "baked" 
    if re.findall(r'saber', asset_folder, re.IGNORECASE):
        if re.findall(r'saber/env/.*/asset', asset_folder, re.IGNORECASE):
            if re.findall(r'baked', asset_folder, re.IGNORECASE):
                return AssetType.SABER_BAKED
            elif re.findall(r'proxy', asset_folder, re.IGNORECASE):
                return AssetType.SABER_PROXY
            elif re.findall(r'merged', asset_folder, re.IGNORECASE):
                return AssetType.SABER_MERGED
            else:
                return AssetType.SABER_ENV
            
        elif re.findall(r'saber/char', asset_folder, re.IGNORECASE):
            return AssetType.SABER_CHAR
        else:
            return AssetType.UNKNOWN
        
    elif re.findall(r'game/disk/env/.*', asset_folder, re.IGNORECASE):
        return AssetType.NRS_REGULAR_ASSET
    else:
        return AssetType.UNKNOWN


class MtlPaths:
    pass


class PathOps:
    LOCAL_SUBFOLDERS = ['Mesh', 'Mat', 'Tex']

    @staticmethod
    def named_asset_folder(asset_folder):
            """Remove local subfolders from asset folder"""
            split = asset_folder.split('/')
            if split[-1] in PathOps.LOCAL_SUBFOLDERS:
                asset_folder = '/'.join(split[:-1])

            return asset_folder

    @staticmethod
    def get_saber_path():
        return unreal.Paths.get_path('/Game/Disk/Saber/')
    
    @staticmethod
    def check_path(path):
        for local_subfolder in PathOps.LOCAL_SUBFOLDERS:
            if path.endswith(local_subfolder):
                raise NameError(f'Path {mtl_folder} is not a valid path')

    @staticmethod
    def construct_mtl_saber_path(asset, asset_type:AssetType):
        asset_name, asset_folder = parse_(asset)
        named_asset_folder = PathOps.named_asset_folder(asset_folder) # without /Mesh, /Mat, ie. /Game/Disk/Saber/Env/TeaHouse/Asset/TeaHouse_Railing_4
        PathOps.check_path(named_asset_folder)

        mtl_path = None 
        
        if asset_type in [AssetType.SABER_BAKED, AssetType.SABER_ENV, AssetType.SABER_PROXY, AssetType.SABER_ENV, AssetType.SABER_CHAR]:
            mtl_path = named_asset_folder + '/Mat'
        
        elif asset_type is AssetType.NRS_REGULAR_ASSET or asset_type is AssetType.NRS_MATERIAL:
            split = named_asset_folder.split('/Disk')
            mtl_path = PathOps.get_saber_path() + split[1] + '/Mat'
        
        return mtl_path
    
    @staticmethod
    def get_mtls_data(asset):
        asset_name, asset_folder = parse_(asset)
        named_asset_folder = PathOps.named_asset_folder(asset_folder)
        asset_type = classify_asset(asset)
        
        mats = material_ops.get_material_slot_names(asset)
        mi = filter_by_class(mats, unreal.MaterialInstanceConstant, debug=True)
        if len(mats) != len(mi):
            unreal.log_error(f'Asset {asset_name} has {len(mats) - len(mi)} non-MI materials')

        mtls_data = []

        if asset_type is AssetType.SABER_MERGED:
            # each mat in its corresponding /Saber/ folder (saving original folder structure i.e. Disk/Env/TehaHouse/Asset/*/Mat)
            for source_mat in mi:
                destination_mtl_path = PathOps.construct_mtl_saber_path(source_mat, AssetType.NRS_MATERIAL)
                mtls_data.append((source_mat, destination_mtl_path))
        else:
            # all mats in one folder
            mtl_path = PathOps.construct_mtl_saber_path(asset, asset_type)

            for source_mat in mi:
                mtls_data.append((source_mat, mtl_path))
        
        return asset_name, named_asset_folder, mtls_data


def set_mi_texture(mi_asset, param_name, tex_path):
    if not unreal.EditorAssetLibrary.does_asset_exist(tex_path):
        unreal.log_warning("Can't find texture: " + tex_path)
        return False
    tex_asset = unreal.EditorAssetLibrary.find_asset_data( tex_path ).get_asset()
    return unreal.MaterialEditingLibrary.set_material_instance_texture_parameter_value(mi_asset, param_name, tex_asset)


def parse_(sm_asset:unreal.Object):
        """Parse asset name and folder"""
        asset_name = sm_asset.get_name()   
        asset_folder = unreal.Paths.get_path(sm_asset.get_path_name())

        if isinstance(sm_asset, unreal.StaticMesh):
            asset_name = asset_name.lstrip('SM_')
        if isinstance(sm_asset, unreal.MaterialInstanceConstant) or isinstance(sm_asset, unreal.Material):
            asset_name = asset_name.lstrip('MI_')
            asset_name = asset_name.lstrip('M_')
        
        re.sub(r'_NX.*|NX.*', '', asset_name)
        
        return asset_name, asset_folder



def filter_by_class(assets, asset_class, debug=False):
    """Filter list of assets by class"""
    filtered = []
    for asset in assets:
        if isinstance(asset, asset_class):
            filtered.append(asset)
        else:
            if debug:
                unreal.log_warning(f"{asset.get_name()} is not {asset_class}")
    return filtered


def prepare_material_folder(folder):
    """Create /Mat/ folder if it doesn't exist"""
    if not unreal.EditorAssetLibrary.does_directory_exist(folder):
        unreal.EditorAssetLibrary.make_directory(folder)
    return folder


def main():
    unreal.log("---------------------------------------------------")
    AssetTools = unreal.AssetToolsHelpers.get_asset_tools()
    MaterialEditingLibrary = unreal.MaterialEditingLibrary
    EditorAssetLibrary = unreal.EditorAssetLibrary
    base_mtl = unreal.EditorAssetLibrary.find_asset_data('/Game/Disk/Saber/Shared/Libs/Mat/Env/BaseMat/M_Env_StaticOpaque_FullyRough.M_Env_StaticOpaque_FullyRough')
        
    #Iterate over selected meshes
    sel_assets = unreal.EditorUtilityLibrary.get_selected_assets()
    sm_assets = filter_by_class(sel_assets, unreal.StaticMesh, debug=True)

    for sm_asset in sm_assets:
        unreal.log_warning(f'--------------------------Processing {sm_asset.get_name()}')
        asset_name, asset_folder, mtls_data = PathOps.get_mtls_data(sm_asset)
        
        # print
        for i, (source_mtl, mtl_new_path) in enumerate(mtls_data):
            unreal.log_warning(f'--------------------------Materials info:')
            unreal.log_warning(f'Source_mat: {source_mtl.get_name()}, new path: {mtl_new_path}')

            tex = material_ops.get_textures(source_mtl)

            if not tex:
                unreal.log_warning(f"Material has no textures assigned: {source_mtl.get_name()}")
                return
            
            mtl_folder = prepare_material_folder(mtl_new_path)

            # name of material instance for this mesh
            mi_name = source_mtl.get_name()            
            mi_full_path = mtl_folder + '/' + mi_name
            
            # Check if material instance already exists
            if EditorAssetLibrary.does_asset_exist(mi_full_path):
                mi_asset = EditorAssetLibrary.find_asset_data(mi_full_path).get_asset()
                unreal.log(f"Material {mi_full_path} already exists, skipping creation...")

                if source_mtl != mi_asset:
                    unreal.log_warning(f"Assigning Material {mi_asset.get_name()}")
                    # assign existing MI to mesh
                    sm_asset.set_material(i, mi_asset)

            else:
                # create MI and assign
                unreal.log("Creating {}")
                mi_asset = AssetTools.create_asset(mi_name, mtl_folder, unreal.MaterialInstanceConstant, unreal.MaterialInstanceConstantFactoryNew())        
        
                # set material instance parameters!
                MaterialEditingLibrary.set_material_instance_parent( mi_asset, base_mtl.get_asset() )  # set parent material
                MaterialEditingLibrary.set_material_instance_texture_parameter_value( mi_asset, "Color", tex[0] ) # set scalar parameter 
            
                # set new material instance on static mesh    
                sm_asset.set_material(i, mi_asset)


main()