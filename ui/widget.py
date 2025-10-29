"""NOT WORKING YET"""

import unreal
from unreal import Vector2D, LinearColor
from unreal import EditorUtilityWidgetBlueprintFactory, TextBlock, Button, SlateColor
# create a new widget blueprint
widget_blueprint = EditorUtilityWidgetBlueprintFactory.create_new(TextBlock, '/Game/MyWidgets/MyWidget')

# create a text block widget
text_block = TextBlock()
text_block.set_text('Hello World!')
text_block.set_color_and_opacity(SlateColor(LinearColor(1, 1, 1)))

# create a button widget
button = Button()
button.set_content_child(text_block)
button.set_size(Vector2D(150, 50))
button.OnClickedEvents.append(lambda: unreal.log('Button clicked!'))

# add the button widget to the blueprint
widget_blueprint.WidgetTree.add_child(button)

# save the blueprint
EditorUtilityWidgetBlueprintFactory. recompile_blueprint(widget_blueprint)

# create an instance of the widget
widget_instance = WidgetBlueprintLibrary.create(widget_blueprint, ue.get_editor_world())

# add the widget to the viewport
WidgetBlueprintLibrary.add_to_viewport(widget_instance)
