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
                        imgui.add_input_text(label="color")
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
                    pass

    def part_drop(self, sender, app_data):
        print(f"drop: {app_data}")
