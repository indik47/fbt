import os
import sys
import unreal
import inspect
from importlib import reload
import re


def main():
    selected_assets = unreal.EditorUtilityLibrary.get_selected_assets()
    skeletals = list(filter(lambda a:type(a) == unreal.SkeletalMesh, selected_assets))
    
    
    def check_(skeletals):
        for skeletal in skeletals:
            physics_asset = skeletal.get_editor_property("physics_asset")
            if not physics_asset:
                unreal.log(f"No phys asset in {skeletal.get_name()}")
            else:
                unreal.log(f"All OK")
    
    
    def find_phys_asset(skeletals):
        for skeletal in skeletals:
            physics_asset = skeletal.get_editor_property("physics_asset")
            if physics_asset:
                return physics_asset
    
    def assign_(skeletals, physics_asset):
        for skeletal in skeletals:
            assigned_physics_asset = skeletal.get_editor_property("physics_asset")
            if not assigned_physics_asset:
                skeletal.set_editor_property("physics_asset", physics_asset)
                unreal.log(f"Assigned {physics_asset.get_fname()} to {skeletal.get_fname()}")
             
    check_(skeletals)
             
    
    # works for selecting all skins for one character i.e. ShaoKahn
    # physics_asset = find_phys_asset(skeletals)
    # if not physics_asset:
    #     unreal.log(f'No phys asset found')
    
    # else:
    #     print(physics_asset.get_fname())
    
    # assign_(skeletals, physics_asset)
    

main()


