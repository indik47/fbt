import unreal

def generate_lods(static_mesh: unreal.StaticMesh, screen_sizes):
    """Generate LODs with provided screen sizes for every LOD"""
    options = unreal.EditorScriptingMeshReductionOptions()
    # Reduction Settings for number of screen sizes array (number of lods). 
    # Percent triangles left at 1.0 (to be set up later)
    options.reduction_settings = [unreal.EditorScriptingMeshReductionSettings(1.0, screen_size) for screen_size in screen_sizes]

    options.auto_compute_lod_screen_size = False
    unreal.EditorStaticMeshLibrary.set_lods(static_mesh, options)

    return True


def apply_lods_batch(data):
    """NOT USED"""
    """Apply LODs reduction to a folder with assets. Options are located in SETTINGS.py. Used this on TeaHouse draft lod application"""
    # all_assets = unreal.EditorAssetLibrary.list_assets(assets_path, recursive=False)
    # all_assets_loaded = [unreal.EditorAssetLibrary.load_asset(a) for a in all_assets]
    # static_mesh_assets = unreal.EditorFilterLibrary.by_class(all_assets_loaded, unreal.StaticMesh)
    # static_mesh_assets = [unreal.load_asset(asset) for asset in assets]
    
    processed_meshes = []
    for (original_staticmesh, NX_staticmesh, screen_sizes) in data:
        if len(screen_sizes) == 1: 
            screen_sizes=[1.0, 0.3, 0.05]

        generate_lods(NX_staticmesh, screen_sizes)
        processed_meshes.append(NX_staticmesh)
    
    return processed_meshes 


def revert_lod0(static_mesh: unreal.StaticMesh):
    """Reverts SM LOD0 to full polycount (in case it was reduced)"""

    lod0 = unreal.EditorStaticMeshLibrary.get_lod_reduction_settings(static_mesh, 0)
    lod0.termination_criterion = unreal.StaticMeshReductionTerimationCriterion.TRIANGLES
    lod0.percent_triangles = 1.0
    lod0.percent_vertices = 1.0
    unreal.EditorStaticMeshLibrary.set_lod_reduction_settings(static_mesh, 0, lod0)


def get_lods_settings(source_staticmesh:unreal.StaticMesh):
    lods_settings = []
    for i in range(source_staticmesh.get_num_lods()):
        current_lod_settings = unreal.EditorStaticMeshLibrary.get_lod_reduction_settings(source_staticmesh, i)
        lods_settings.append(current_lod_settings)
    
    return lods_settings


def apply_lods_settings(lods_settings, mesh2: unreal.StaticMesh):
    for i, mesh_reduction_settings in enumerate(lods_settings):
        unreal.EditorStaticMeshLibrary.set_lod_reduction_settings(mesh2, i, mesh_reduction_settings)


def apply_def_lods_settings(startLOD: int, endLOD:int, mesh: unreal.StaticMesh, def_settings: list):
    for i in range(startLOD, endLOD):
        unreal.EditorStaticMeshLibrary.set_lod_reduction_settings(mesh, i, def_settings[i])

