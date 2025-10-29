import unreal

dialog = unreal.DialogBuilder()
dialog.set_title("Material Options")
dialog.set_buttons(unreal.ModalDialogButtons.OK_CANCEL)
# if args.nodepath:
#     picked_node = dialog.add_combo_box("Select a Node", paths, rchop(args.nodepath, ".Root"));
# else:

picked_node = dialog.add_combo_box("Select a Node", ['ONE', 'TWO', 'THREE']);
picked_param = dialog.add_text_box("Parameter Name:", "", "i.e. Effect Amount" );
picked_type = dialog.add_combo_box("Select a Parameter Type",{'scalar_item', 'vector_item'});
attach_to_bone = dialog.add_check_box("Attach to Bone", False);
modal_result = dialog.show_modal();