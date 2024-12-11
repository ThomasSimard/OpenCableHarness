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

    str_to_color = {
        "Black": (0, 0, 0, 255),
        "Red": (255, 0, 0, 255),
        "White": (255, 255, 255, 255),
        "Blue": (0, 0, 255, 255),
        "Green": (0, 255, 0, 255)
    }

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
        imgui.add_button(label="Save project")

        imgui.add_button(label="Close project",
            user_data=self.name, callback=close_project_tab)

    def wire(self):
        "Wire editor"
        imgui.add_text("", tag="wire_error_label", color=(250, 100, 120))

        imgui.add_text("Add wire")
        imgui.add_input_text(label="name", tag=f"{self.name}_input_name")

        imgui.add_listbox(tag=f"{self.name}_color_list",
            items=[key for key in self.str_to_color],
            num_items=len(self.str_to_color))

        imgui.add_color_edit(no_alpha=True)

        imgui.add_input_int(label="awg",
            default_value=20, min_value=1, min_clamped=True,
            tag=f"{self.name}_input_awg")

        imgui.add_button(label="Add", callback=self.add_wire)

        imgui.add_separator()

        imgui.add_text("Wire list")

        with imgui.child_window(width=200):
            with imgui.table(tag=f"{self.name}_wire_list"):
                imgui.add_table_column(label="Color", width=25, width_fixed=True)
                imgui.add_table_column(label="Name")
                imgui.add_table_column(label="Awg", width=25, width_fixed=True)

        #imgui.add_listbox([], tag=f"{self.name}_wire_list",
        #    callback=self.wire_selected)

        #with imgui.drag_payload(parent=f"{self.name}_wire_list",
        #    tag=f"{self.name}_wire_list_payload",
        #    drag_data=imgui.get_value(f"{self.name}_wire_list"),
        #    payload_type="wire"):

        #    imgui.add_text(imgui.get_value(f"{self.name}_wire_list"),
        #        tag=f"{self.name}_wire_list_payload_label")

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

    def add_wire(self):
        name = imgui.get_value(f"{self.name}_input_name")
        color = imgui.get_value(f"{self.name}_color_list")
        awg = imgui.get_value(f"{self.name}_input_awg")

        if name == "":
            print("error")

        self.project_info.wires.add(name, (color, awg))

        with imgui.table_row(parent=f"{self.name}_wire_list"):
            imgui.add_color_button(default_value=self.str_to_color[color])

            imgui.add_text(name)

            imgui.add_text(awg)


    def wire_selected(self, _, wire):
        imgui.configure_item(f"{self.name}_wire_list_payload", drag_data=wire)
        imgui.set_value(f"{self.name}_wire_list_payload_label", wire)

    def part_drop(self, sender, part):
        "Make nodes from draging part"
