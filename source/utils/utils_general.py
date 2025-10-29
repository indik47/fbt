import os
import sys
import subprocess
import platform
import unreal
import re

FILEBROWSER_PATH = os.path.join(os.getenv("WINDIR"), "explorer.exe")
NOTEPAD_PATH = r"C:\Program Files (x86)\Notepad++\notepad++.exe"


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


def prepare_dir(dir):
    """Create dir if it doesn't exist"""
    if not unreal.EditorAssetLibrary.does_directory_exist(dir):
        unreal.EditorAssetLibrary.make_directory(dir)
    return dir


def explore(path):
    """Path can be a directory or a file
        directory -> open directory in WinExplorer
        file -> open in Notepad++"""

    # explorer would choke on forward slashes
    path = os.path.normpath(path)

    if os.path.exists(path):
        if os.path.isdir(path):
                if platform.system() == "Windows":
                    os.startfile(path)
                    
        elif os.path.isfile(path):
            subprocess.run([NOTEPAD_PATH, path])


def inspect_fame():
    caller = sys._getframe(1)  # Obtain calling frame
    unreal.log("Called from module" + caller.f_globals['__name__'])
    unreal.log("File is " + os.path.dirname( __file__ ))
    unreal.log(__name__)
