"""Project window"""
import dearpygui.dearpygui as imgui

from datasave import DataSave

from app.nodeeditor import NodeEditor

from components import Wire

class ProjectWindow:
    "Tab to edit the project"

    def __init__(self, name, close_project_tab):
        self.name = name
        self.save = DataSave(f"projects/{self.name}.json")

        with imgui.group(horizontal=True):
            with imgui.group(width=150):
                self.project_settings(close_project_tab)

                imgui.add_separator()

                with imgui.tab_bar():
                    with imgui.tab(label="Wire"):
                        self.wire()

            with imgui.tab_bar():
                with imgui.tab(label="Node editor",
                    drop_callback=self.part_drop, payload_type="part"):

                    NodeEditor(self.name, self.save)
                with imgui.tab(label="BOM"):
                    with imgui.child_window():
                        self.bill_of_material()

    def project_settings(self, close_project_tab):
        "Project settings UI"
        imgui.add_text("Project settings")
        imgui.add_button(label="Save project") #TODO : Manual save project

        imgui.add_button(label="Export project") #TODO : Export project as pdf

        imgui.add_button(label="Close project",
            user_data=self.name, callback=close_project_tab)

    def wire(self):
        "Wire editor"
        imgui.add_text("", tag=f"{self.name}_wire_error_label", color=(250, 100, 120))

        imgui.add_text("Add wire")
        imgui.add_input_text(label="name", tag=f"{self.name}_input_name")

        imgui.add_listbox(tag=f"{self.name}_color_list",
            items=[key for key in Wire.str_to_color],
            num_items=len(Wire.str_to_color))

        imgui.add_color_edit(no_alpha=True)

        imgui.add_input_int(label="awg",
            default_value=20, min_value=1, min_clamped=True,
            tag=f"{self.name}_input_awg")

        imgui.add_button(label="Add", callback=self.add_wire)

        imgui.add_separator()

        imgui.add_text("Wire list")

        with imgui.child_window(width=200):
            Wire.table_header(self.name)

        self.load_wires()

    def bill_of_material(self):
        "BOM"

        with imgui.table():
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

    def load_wires(self):
        for wire_name in self.save.get_children("wire"):
            wire = Wire(
                wire_name,
                self.save["wire", wire_name][0],
                self.save["wire", wire_name][1])

            wire.add_to_table(self.name)

    def add_wire(self):
        name = imgui.get_value(f"{self.name}_input_name")
        color = imgui.get_value(f"{self.name}_color_list")
        gauge = imgui.get_value(f"{self.name}_input_awg")

        wire = Wire(name, color, gauge)

        status = self.save.check_tag_integrity(f"wire_{name}")
        imgui.set_value(f"{self.name}_wire_error_label", status)

        if status == "":
            self.save["wire", name] = (color, gauge)
            wire.add_to_table(self.name)

    def part_drop(self, sender, part):
        "Make nodes from draging part"
        # TODO : Implement fonction
