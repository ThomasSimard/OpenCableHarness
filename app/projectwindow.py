"""Project window"""
import dearpygui.dearpygui as dpg

from widget.swisscontrols.DataGrid import DataGrid
from widget.swisscontrols.ListEditCtrl import listEditCtrl

from datasave import DataSave

from app.nodeeditor import NodeEditor

from components import Wire

class ProjectWindow:
    "Tab to edit the project"

    def __init__(self, name, close_project_tab):
        self.name = name
        self.save = DataSave(f"projects/{self.name}.json")

        with dpg.group(horizontal=True):
            with dpg.group(width=200):
                self.project_settings(close_project_tab)

                dpg.add_separator()

                with dpg.tab_bar():
                    with dpg.tab(label="Wire"):
                        self.wire()

            with dpg.tab_bar():
                with dpg.tab(label="Node editor",
                    drop_callback=self.part_drop, payload_type="part"):

                    NodeEditor(self.name, self.save)
                with dpg.tab(label="BOM"):
                    with dpg.child_window():
                        self.bill_of_material()

    def project_settings(self, close_project_tab):
        "Project settings UI"
        with dpg.child_window(menubar=True, height=150):
            with dpg.menu_bar():
                dpg.add_text("Project settings")

            dpg.add_button(label="Save project") #TODO : Manual save project

            dpg.add_button(label="Export project") #TODO : Export project as pdf

            dpg.add_button(label="Close project",
                user_data=self.name, callback=close_project_tab)

    def wire(self):
        "Wire editor"

        wire_grid = DataGrid(
            title="Wire editor",
            columns = ['Color', 'Name', 'Gauge'],
            dtypes = [DataGrid.COLOR, DataGrid.TXT_STRING, DataGrid.COMBO],
            defaults = [False, "New wire", 0],
            combo_lists = [None, None, ["Avacado", "Banana", "Lemon", "Pear"]]
        )

        with dpg.group(width=200):
            id_fruits = dpg.generate_uuid()
            eval_grid = listEditCtrl(id_fruits, grid=wire_grid)

        """dpg.add_text("", tag=f"{self.name}_wire_error_label", color=(250, 100, 120))

        dpg.add_text("Add wire")
        dpg.add_input_text(label="name", tag=f"{self.name}_input_name")

        dpg.add_listbox(tag=f"{self.name}_color_list",
            items=[key for key in Wire.str_to_color],
            num_items=len(Wire.str_to_color))

        dpg.add_color_edit(no_alpha=True)

        dpg.add_input_int(label="awg",
            default_value=20, min_value=1, min_clamped=True,
            tag=f"{self.name}_input_awg")

        dpg.add_button(label="Add", callback=self.add_wire)

        dpg.add_separator()

        dpg.add_text("Wire list")

        with dpg.child_window(width=200):
            Wire.table_header(self.name)

        self.load_wires()"""

    def bill_of_material(self):
        "BOM"

        with dpg.table():
            dpg.add_table_column(label="Name")
            dpg.add_table_column(label="Manufacturer")
            dpg.add_table_column(label="Quantity")

            # add_table_next_column will jump to the next row
            # once it reaches the end of the columns
            # table next column use slot 1
            for i in range(0, 4):
                with dpg.table_row():
                    for j in range(0, 3):
                        dpg.add_text(f"Row{i} Column{j}")

    def load_wires(self):
        for wire_name in self.save.get_children("wire"):
            wire = Wire(
                wire_name,
                self.save["wire", wire_name][0],
                self.save["wire", wire_name][1])

            wire.add_to_table(self.name)

    def add_wire(self):
        name = dpg.get_value(f"{self.name}_input_name")
        color = dpg.get_value(f"{self.name}_color_list")
        gauge = dpg.get_value(f"{self.name}_input_awg")

        wire = Wire(name, color, gauge)

        status = self.save.check_tag_integrity(f"wire_{name}")
        dpg.set_value(f"{self.name}_wire_error_label", status)

        if status == "":
            self.save["wire", name] = (color, gauge)
            wire.add_to_table(self.name)

    def part_drop(self, sender, part):
        "Make nodes from draging part"
        # TODO : Implement fonction
