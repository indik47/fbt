import unreal
import copy
import itertools
import datetime

RESOLUTION = [1920, 1080]
# Example simple script that uses existing camera actors by name,
# pilots each one, and takes a HighResScreenshot.

camera_names = [
        "VP_1",
        "VP_2",
        "VP_3",
        "VP_4",
        "VP_5",
        "VP_6",
        "VP_7",
        "VP_8",
        "VP_9",
    ]

def find_cameras():
    cameras = []
    editor_actor_subsys = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    sel_actors = editor_actor_subsys.get_selected_level_actors()
    
    for cam_name in camera_names:
        for actor in sel_actors:
            if actor.get_actor_label() == cam_name:
                cameras.append(actor)
                break
    
    return cameras

class OnTick(object):
    def __init__(self, cameras):
        
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
            date = datetime.datetime.now().strftime("%d_%m")  # date in format "31_01"
            savename = f'{camera.get_actor_label()}_{date}.png'
            unreal.AutomationLibrary.take_high_res_screenshot(RESOLUTION[0], RESOLUTION[1], savename)

        except Exception as error:
            unreal.unregister_slate_pre_tick_callback(self.on_tick_delegate_handle)


def main():
    OnTick(find_cameras())
    
    
main()
