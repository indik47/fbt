import unreal 
import os
import sys
import inspect

thispath = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
if thispath not in sys.path:
    sys.path.append(thispath)

# save actors selection to a file
def get_sel_actors():
    sel_actors = unreal.EditorLevelLibrary.get_selected_level_actors()
    sel_actors_names = []
    for actor in sel_actors:
        sel_actors_names.append(actor.get_name())
    return sel_actors_names


#deselect all actors
unreal.EditorLevelLibrary.deselect_all_actors()

selected = get_sel_actors()

if selected:
    print(selected[0])

# # select previously selected actors
# for actor_name in selected:
#     actor = unreal.EditorLevelLibrary.find_actor_by_label(actor_name)
#     if actor:
#         actor.select()
