"""Project window"""

import dearpygui.dearpygui as imgui

from app.nodeeditor import NodeEditor

class ProjectWindow:
    "Tab to edit the project"

    cable_list = []
    node_list = []

    def __init__(self, name):
        self.name = name

        with imgui.group(horizontal=True):
            with imgui.group(width=150):
                imgui.add_text("Project settings")
                imgui.add_button(label="Save project")

                imgui.add_separator()

                with imgui.tab_bar():
                    with imgui.tab(label="Wire"):
                        imgui.add_text("Add wire")
                        imgui.add_input_text(label="name")

                        imgui.add_color_picker(
                            no_alpha=True, picker_mode=imgui.mvColorPicker_wheel)

                        imgui.add_input_int(label="awg",
                            default_value=20, min_value=1, min_clamped=True)

                        imgui.add_button(label="Add")

                        imgui.add_separator()

                        imgui.add_text("Wire list")
                        imgui.add_listbox([1, 2, 3, 4, 5], tag="wire_list", callback=self.wire_selected)

                        with imgui.drag_payload(parent="wire_list", tag="wire_list_payload",
                            drag_data=imgui.get_value("wire_list"), payload_type="wire"):

                            imgui.add_text(imgui.get_value("wire_list"), tag="wire_list_payload_label")

            with imgui.tab_bar():
                with imgui.tab(label="Node editor",
                    drop_callback=self.part_drop, payload_type="part"):

                    NodeEditor(self.name)
                with imgui.tab(label="BOM"):
                    with imgui.child_window():
                        with imgui.table():

                            # use add_table_column to add columns to the table,
                            # table columns use child slot 0
                            imgui.add_table_column(label="Name")
                            imgui.add_table_column(label="Manufacturer")
                            imgui.add_table_column(label="Quantity")

                            # add_table_next_column will jump to the next row
                            # once it reaches the end of the columns
                            # table next column use slot 1
                            for i in range(0, 4):
                                with imgui.table_row():
                                    for j in range(0, 3):
                                        imgui.add_text(f"Row{i} Column{j}")

    def wire_selected(self, _, wire):
        imgui.configure_item("wire_list_payload", drag_data=wire)
        imgui.set_value("wire_list_payload_label", wire)

    def part_drop(self, sender, part):
        "Make nodes from draging part"
