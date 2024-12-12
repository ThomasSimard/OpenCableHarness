"""Project window"""
import dearpygui.dearpygui as imgui

from savefile import SaveFile

from app.nodeeditor import NodeEditor

from components import Wire

class ProjectWindow:
    "Tab to edit the project"

    class ProjectInfo:
        "All the project info to be saved"

        class Data:
            "Check data validity"
            data_dict = dict()

            def __init__(self, data, save):
                self.data_dict = data
                self.save = save

            def add(self, name, data):
                "Add data to the dict with checks"

                if name == "":
                    return "Name cannot be empty!"
                elif name in self.data_dict:
                    return "Name already exists!"
                else:
                    self.data_dict.update({name: data})
                    self.save()

                return ""

        def __init__(self, name):
            self.name = name
            self.project_save = SaveFile(f"projects/{self.name}")

            if len(self.project_save.data) > 0:
                self.wires = self.Data(self.project_save.data[0], self.save)
            else:
                self.wires = self.Data({}, self.save)

        def save(self):
            "Save project info"
            data = (self.wires.data_dict, 0)

            self.project_save.replace(data)

    def __init__(self, name, close_project_tab):
        self.name = name
        self.project_info = self.ProjectInfo(self.name)

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

                    NodeEditor(self.name)
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
        for wire_name in self.project_info.wires.data_dict:
            wire = Wire(
                wire_name,
                self.project_info.wires.data_dict[wire_name][0],
                self.project_info.wires.data_dict[wire_name][1])

            wire.add_to_table(self.name)

    def add_wire(self):
        name = imgui.get_value(f"{self.name}_input_name")
        color = imgui.get_value(f"{self.name}_color_list")
        gauge = imgui.get_value(f"{self.name}_input_awg")

        wire = Wire(name, color, gauge)
        status = self.project_info.wires.add(name, (color, gauge))

        if status == "":
            wire.add_to_table(self.name)

        imgui.set_value(f"{self.name}_wire_error_label", status)

    def part_drop(self, sender, part):
        "Make nodes from draging part"
        # TODO : Implement fonction
