import unreal

DISM_LODS_SETTINGS = [
{   'lod': 0,
    'base_lod': 0,
    'number_of_verts': 1500,
    'screen_size': 1.0
},
{   'lod': 1,
    'base_lod': 0,
    'number_of_verts': 499,
    'screen_size': 0.3
}
]

GEAR_LODS_SETTINGS = [
{   'lod': 0,
    'base_lod': 0,
    'number_of_verts': 1500,
    'screen_size': 1.0
},
{   'lod': 1,
    'base_lod': 0,
    'number_of_verts': 499,
    'screen_size': 0.3
},
{   'lod': 2,
    'base_lod': 0,
    'number_of_verts': 499,
    'screen_size': 0.3
},
]

DEFAULT_LODs_SCREEN_SIZES = [1.0, 0.3, 0.05]
DEFAULT_LODs_SETTINGS = [
                unreal.MeshReductionSettings(percent_triangles=1.0, percent_vertices=1.0, termination_criterion=unreal.StaticMeshReductionTerimationCriterion.VERTICES),
                unreal.MeshReductionSettings(percent_triangles=1.0, percent_vertices=0.5, termination_criterion=unreal.StaticMeshReductionTerimationCriterion.VERTICES),
                unreal.MeshReductionSettings(percent_triangles=1.0, percent_vertices=0.1, termination_criterion=unreal.StaticMeshReductionTerimationCriterion.VERTICES),
                ]

TeaHouse_dirs_december_setup  = [
                # "/Game/Disk/Env/TeaHouse/Asset/TeaHouse_Table/Mesh",
                # "/Game/Disk/Env/TeaHouse/Asset/TeaHouse_WoodSlats/Mesh",
                # "/Game/Disk/Env/TeaHouse/Asset/TeaHouse_Railing/Mesh",
                # "/Game/Disk/Env/TeaHouse/Asset/TeaHouse_Roof/Mesh/" ,
                # "/Game/Disk/Env/TeaHouse/Asset/TeaHouse_LargePillar/Mesh",
                # "/Game/Disk/Env/TeaHouse/Asset/TeaHouse_WoodenBeams/Mesh",
                # "/Game/Disk/Env/TeaHouse/Asset/TeaHouse_DiningRoomWalls/Mesh",
                # "/Game/Disk/Env/TeaHouse/Asset/TeaHouse_HangLantern/Mesh",
                # "/Game/Disk/Env/TeaHouse/Asset/TeaHouse_Doorway/Mesh",
                # "/Game/Disk/Env/TeaHouse/Asset/TeaHouse_GlassJars/Mesh",
                # "/Game/Disk/Env/TeaHouse/Asset/TeaHouse_SmallAcc/Mesh",
                # "/Game/Disk/Env/TeaHouse/Asset/TeaHouse_Birdcage/Mesh",
                # "/Game/Disk/Env/TeaHouse/Asset/TeaHouse_Clothes/Mesh", 
                # "/Game/Disk/Env/TeaHouse/Asset/TeaHouse_Plants/Mesh"
                ] 


TeaHouse_folders  = [
                # "/Game/Disk/Env/TeaHouse/Asset/TeaHouse_AngledShelf/Mesh",
                # "/Game/Disk/Env/TeaHouse/Asset/TeaHouse_Antenna/Mesh",
                # "/Game/Disk/Env/TeaHouse/Asset/TeaHouse_Bucket/Mesh",
                # "/Game/Disk/Env/TeaHouse/Asset/TeaHouse_Cardboard/Mesh",
                # "/Game/Disk/Env/TeaHouse/Asset/TeaHouse_CeilingFan/Mesh",
                # "/Game/Disk/Env/TeaHouse/Asset/TeaHouse_CookingTable/Mesh",
                # "/Game/Disk/Env/TeaHouse/Asset/TeaHouse_Chair/Mesh",
                # "/Game/Disk/Env/TeaHouse/Asset/TeaHouse_ConcreteFloor/Mesh",
                # "/Game/Disk/Env/TeaHouse/Asset/TeaHouse_Counter/Mesh",
                # "/Game/Disk/Env/TeaHouse/Asset/TeaHouse_CounterProps/Mesh",
                # "/Game/Disk/Env/TeaHouse/Asset/TeaHouse_CounterRetail/Mesh",
                # "/Game/Disk/Env/TeaHouse/Asset/TeaHouse_CrateA/Mesh",
                # "/Game/Disk/Env/TeaHouse/Asset/TeaHouse_Curtains/Mesh",
                # "/Game/Disk/Env/TeaHouse/Asset/TeaHouse_DiningRoomWalls/Mesh",
                # "/Game/Disk/Env/TeaHouse/Asset/TeaHouse_Dragon/Mesh",
                # "/Game/Disk/Env/TeaHouse/Asset/TeaHouse_Floor/Mesh",
                # "/Game/Disk/Env/TeaHouse/Asset/TeaHouse_Fluorescent/Mesh",
                # "/Game/Disk/Env/TeaHouse/Asset/TeaHouse_FridgeVert/Mesh",
                # "/Game/Disk/Env/TeaHouse/Asset/TeaHouse_Fryer/Mesh",
                # "/Game/Disk/Env/TeaHouse/Asset/TeaHouse_GrainSacks/Mesh",
                # "/Game/Disk/Env/TeaHouse/Asset/TeaHouse_HangLantern/Mesh",
                # "/Game/Disk/Env/TeaHouse/Asset/TeaHouse_HorizontalFridge/Mesh",
                # "/Game/Disk/Env/TeaHouse/Asset/TeaHouse_KitchenProps/Mesh",
                # "/Game/Disk/Env/TeaHouse/Asset/TeaHouse_KnifeShelf/Mesh",
                # "/Game/Disk/Env/TeaHouse/Asset/TeaHouse_Ladder/Mesh",
                # "/Game/Disk/Env/TeaHouse/Asset/TeaHouse_LargeCounter/Mesh",
                # "/Game/Disk/Env/TeaHouse/Asset/TeaHouse_LargePosters/Mesh",
                # "/Game/Disk/Env/TeaHouse/Asset/TeaHouse_Leaves/Mesh",
                # "/Game/Disk/Env/TeaHouse/Asset/TeaHouse_LowWall/Mesh",
                # "/Game/Disk/Env/TeaHouse/Asset/TeaHouse_OilLamp/Mesh",
                # "/Game/Disk/Env/TeaHouse/Asset/TeaHouse_OutdoorTrellis/Mesh",
                # "/Game/Disk/Env/TeaHouse/Asset/TeaHouse_Pendant/Mesh",
                # "/Game/Disk/Env/TeaHouse/Asset/TeaHouse_Pipes/Mesh",
                # "/Game/Disk/Env/TeaHouse/Asset/TeaHouse_PorcelainDoll/Mesh",
                # "/Game/Disk/Env/TeaHouse/Asset/TeaHouse_Railing/Mesh",
                # "/Game/Disk/Env/TeaHouse/Asset/TeaHouse_RiceJar/Mesh",
                # "/Game/Disk/Env/TeaHouse/Asset/TeaHouse_Rugs/Mesh",
                # "/Game/Disk/Env/TeaHouse/Asset/TeaHouse_Screen/Mesh",
                # "/Game/Disk/Env/TeaHouse/Asset/TeaHouse_Shelf/Mesh",
                # "/Game/Disk/Env/TeaHouse/Asset/TeaHouse_Sink/Mesh",
                # "/Game/Disk/Env/TeaHouse/Asset/TeaHouse_Stairs/Mesh",
                # "/Game/Disk/Env/TeaHouse/Asset/TeaHouse_StringLights/Mesh",
                # "/Game/Disk/Env/TeaHouse/Asset/TeaHouse_TableCloth/Mesh",
                # "/Game/Disk/Env/TeaHouse/Asset/TeaHouse_TableProps/Mesh",
                # "/Game/Disk/Env/TeaHouse/Asset/TeaHouse_TeaBar/Mesh",
                # "/Game/Disk/Env/TeaHouse/Asset/TeaHouse_TeaKettle/Mesh",
                # "/Game/Disk/Env/TeaHouse/Asset/TeaHouse_TeaStove/Mesh",
                # "/Game/Disk/Env/TeaHouse/Asset/TeaHouse_TeaWalkway/Mesh",
                # "/Game/Disk/Env/TeaHouse/Asset/TeaHouse_TrashCan/Mesh",
                # "/Game/Disk/Env/TeaHouse/Asset/TeaHouse_TV/Mesh",
                # "/Game/Disk/Env/TeaHouse/Asset/TeaHouse_VentFan/Mesh",
                # "/Game/Disk/Env/TeaHouse/Asset/TeaHouse_Walls/Mesh",
                # "/Game/Disk/Env/TeaHouse/Asset/TeaHouse_WickerThermos/Mesh",
                # "/Game/Disk/Env/TeaHouse/Asset/TeaHouse_WindChime/Mesh",
                # "/Game/Disk/Env/TeaHouse/Asset/TeaHouse_WoodBench/Mesh",
                # "/Game/Disk/Env/TeaHouse/Asset/TeaHouse_WoodenBeams/Mesh",
                # "/Game/Disk/Env/TeaHouse/Asset/TeaHouse_WoodenPallet/Mesh",
                "/Game/Disk/Env/TeaHouse/Asset/TeaHouse_WoodLantern/Mesh",
                ] 

TeaHouse_exclusion_folders = [
                "/Game/Disk/Env/TeaHouse/Asset/TeaHouse_Mountains/Mesh",
                "/Game/Disk/Env/TeaHouse/Asset/TeaHouse_NPC_Blockouts/Mesh",
                "/Game/Disk/Env/TeaHouse/Asset/TeaHouse_Lighting/Mesh",
                "/Game/Disk/Env/TeaHouse/Asset/TeaHouse_Landscape/Mesh",
                "/Game/Disk/Env/TeaHouse/Asset/TeaHouse_PreLighting/Mesh",
                "/Game/Disk/Env/TeaHouse/Asset/TeaHouse_Rain/Mesh",
                "/Game/Disk/Env/TeaHouse/Asset/TeaHouse_Skydome/Mesh",
                "/Game/Disk/Env/TeaHouse/Asset/TeaHouse_Supermove/Mesh",
                "/Game/Disk/Env/TeaHouse/Asset/TeaHouse_Trees/Mesh",
                "/Game/Disk/Env/TeaHouse/Asset/TeaHouse_Vista/Mesh",
                "/Game/Disk/Env/TeaHouse/Asset/TeaHouse_Volumetrics/Mesh",
                "/Game/Disk/Env/TeaHouse/Asset/TeaHouse_WallDeco/Mesh",
                        ]