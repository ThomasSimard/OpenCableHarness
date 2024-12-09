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
                    with imgui.tab(label="Cable"):
                        imgui.add_text("Add cable")
                        imgui.add_input_text(label="name")

                        imgui.add_color_picker(
                            no_alpha=True, picker_mode=imgui.mvColorPicker_wheel)

                        imgui.add_input_int(label="awg")

                        imgui.add_button(label="Add")

                        imgui.add_separator()

                        imgui.add_text("Cable list")
                        imgui.add_listbox([1, 2, 3, 4])

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

    def part_drop(self, sender, part):
        "Make nodes from draging part"
