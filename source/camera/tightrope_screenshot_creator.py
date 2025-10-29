import sys
import unreal
import copy
import itertools

RESOLUTION = [1920, 1080]
CAM_NUMBER = 3

# Default = 22.58. This equals 55mm FoV
FOCAL_LENGTH = 12.58

# Default = 350
OFFSET_BACK_FROM_TIGHTROPE = 350 
# Default = 120
OFFSET_UP_FROM_TIGHTROPE = 120
# Default = 0
OFFSET_LEFT_FROM_TIGHTROPE = 0
# Default = 0
OFFSET_RIGHT_FROM_TIGHTROPE = 200


@unreal.uclass()
class MyEditorLvelLib(unreal.EditorLevelLibrary):
    pass


class LevelManager:
    @staticmethod
    def filter_by_class(actors, class_type):
        return [actor for actor in actors if actor.get_class() == class_type]

    @staticmethod
    def get_tightrope():
        allLevelActors = MyEditorLvelLib().get_all_level_actors()
        for actor in allLevelActors:
            if 'tightrope' in actor.get_name().lower():
                return actor

            else:
                return None

    @staticmethod
    def get_current_level():
        curr_lvl = unreal.EditorLevelLibrary.get_editor_world().get_name()

        return curr_lvl


class CameraManager:
    CAMERAS = []

    @staticmethod
    def get_stream_name():
        version = unreal.SystemLibrary.get_engine_version()
        stream = ''
        if 'switch' in version.lower():
            stream = 'Switch'
        if 'main' in version.lower():
            stream = 'Main'

        return stream


    @staticmethod
    def create_camera(stream, lightscenario, location, rotation, y_offset=0.0):
        actor_class = unreal.CineCameraActor
        actor_location = copy.copy(location) # + (actor.get_actor_right_vector() * 200) #move it slightly to the front of the character
        actor_location.z = OFFSET_UP_FROM_TIGHTROPE #move on up vec (z)
        actor_location.x -= OFFSET_BACK_FROM_TIGHTROPE
        actor_location.y = y_offset

        _spawnedActor = unreal.EditorLevelLibrary.spawn_actor_from_class(actor_class, actor_location, rotation)
        _focusSettings = unreal.CameraFocusSettings()
        _focusSettings.manual_focus_distance = 1320.0
        _focusSettings.focus_method = unreal.CameraFocusMethod.MANUAL
        _focusSettings.focus_offset = 19.0
        _focusSettings.smooth_focus_changes = False

        _cineCameraComponent = _spawnedActor.get_cine_camera_component()
        _cineCameraComponent.set_editor_property("focus_settings", _focusSettings)

        _spawnedActor.set_actor_label(f'{lightscenario}_{_spawnedActor.get_name()}_{stream}')

        return _spawnedActor

    @classmethod
    def create_cameras(cls, lightscenario):        
        tightrope = LevelManager.get_tightrope()
        
        stream = cls.get_stream_name()

        if tightrope:
            location = tightrope.get_actor_location()
            rotation = tightrope.get_actor_rotation()

            TIGHTROPE_LEFT = -1000 + OFFSET_LEFT_FROM_TIGHTROPE
            TIGHTROPE_RIGHT = 1000 - OFFSET_RIGHT_FROM_TIGHTROPE
            TIGHTROPE_LENGTH = TIGHTROPE_RIGHT - TIGHTROPE_LEFT

            DIVISIONS = CAM_NUMBER - 1
            if DIVISIONS == 0:
                y_offsets = [0]
            else:
                step = int(TIGHTROPE_LENGTH / (CAM_NUMBER-1))
                y_offsets = [TIGHTROPE_LEFT + i*step for i in range(CAM_NUMBER)]
            
            for y_offset in y_offsets:
                camera = CameraManager.create_camera(stream, lightscenario, location, rotation, y_offset)
                camera_component = camera.get_cine_camera_component()
                camera_component.set_editor_property('current_focal_length', FOCAL_LENGTH)

                cls.CAMERAS.append(camera)
            
            return cls.CAMERAS


class OnTick(object):
    def __init__(self, cameras, lightscenarios, lscenarios_levels_data):
        
        self.lightscenarios = lightscenarios
        self.lscenarios_levels_data = lscenarios_levels_data
        self.cameras = iter(cameras)
        self.cameras_to_destroy = copy.copy(cameras)
        self.on_tick_delegate_handle = unreal.register_slate_pre_tick_callback(self.__make_screenshot__)

        self.tick_count = 0
    
    def __make_screenshot__(self, delta_time):
        """ Every tick callback"""
        try:
            self.tick_count += 1
            camera = next(self.cameras)
            unreal.EditorLevelLibrary.pilot_level_actor(camera)

            ls = camera.get_name().split('_')[0]  # from camera name. HACK, need to rewrite to work with delegate correctly
            
            if ls not in self.lightscenarios:
                unreal.log_error('RETURN ls not in lightscenarios {ls}')
                return
            
            LightScenarioManager.activate_light_scenario(self.lscenarios_levels_data, ls)
            unreal.AutomationLibrary.take_high_res_screenshot(RESOLUTION[0], RESOLUTION[1], f'{camera.get_name()}.png')

        except Exception as error:
            unreal.unregister_slate_pre_tick_callback(self.on_tick_delegate_handle)
            for c in self.cameras_to_destroy:
                unreal.EditorLevelLibrary.destroy_actor(c)
            

class LightScenarioManager:
    @staticmethod
    def get_levels():
        world = unreal.EditorLevelLibrary.get_editor_world()
        levels = unreal.EditorLevelUtils.get_levels(world)

        return world, levels

    @staticmethod
    def parse_level_name(level):
        pathname = level.get_path_name()
        name = pathname.split('/')[-1].split('.')[0]

        return name

    @staticmethod
    def get_light_scenarios_names():
        def filter_lighting_levels(levels):
            light_levels = []
            for level in levels:
                pathname = level.get_path_name()
                if '_Lighting_' in pathname and '_NX' not in pathname:
                    light_levels.append(level)

            return light_levels

        world, levels = LightScenarioManager.get_levels()
        lighting_levels = filter_lighting_levels(levels)
        
        scenarios = []
        for l in lighting_levels:
            pathname = l.get_path_name()
            name = pathname.split('/')[-1].split('.')[0].split('_Lighting_')[-1]
            scenarios.append(name)
        
        if len(scenarios) < 2 or len(scenarios) > 3:
            unreal.log_warning("Lighting scenarios not found")
            return None

        return scenarios

    @staticmethod
    def get_light_scenarios_levels():
        world, levels = LightScenarioManager.get_levels()

        lightscenario_levels = {}
        for ligthscenario in LightScenarioManager.get_light_scenarios_names():
            lightscenario_levels[ligthscenario] = []

            for level in levels:
                pathname = level.get_path_name()
                if ligthscenario in pathname and '_NX' not in pathname:
                    lightscenario_levels[ligthscenario].append(level)
        
        return lightscenario_levels

    @staticmethod
    def make_visible(current, other):
        for level in current:
            unreal.EditorLevelUtils.set_level_visibility(level, should_be_visible=True, force_layers_visible=True, modify_mode=unreal.LevelVisibilityDirtyMode.DONT_MODIFY)    
        for level in other:
            unreal.EditorLevelUtils.set_level_visibility(level, should_be_visible=False, force_layers_visible=False, modify_mode=unreal.LevelVisibilityDirtyMode.DONT_MODIFY)

    @staticmethod
    def activate_light_scenario(lscenarios_levels_data, lightscenario):
        current_lscenario_levels = lscenarios_levels_data[lightscenario]
        all_levels = [l for l in lscenarios_levels_data.values()]
        all_levels = list(itertools.chain.from_iterable(all_levels)) # flatten list of lists
        other_lscenarios_levels = [l for l in all_levels if l not in current_lscenario_levels]

        LightScenarioManager.make_visible(current_lscenario_levels, other_lscenarios_levels)


def main():
    unreal.log_warning(f'{"-"*10}Starting Screenshot Creator script{"-"*10}')

    lscenarios_levels_data = LightScenarioManager.get_light_scenarios_levels()
    lscenarios = list(lscenarios_levels_data.keys())

    for lightscenario in lscenarios:
        ls_cameras = CameraManager.create_cameras(lightscenario)
    
    ontick = OnTick(CameraManager.CAMERAS, lscenarios, lscenarios_levels_data)


main()
