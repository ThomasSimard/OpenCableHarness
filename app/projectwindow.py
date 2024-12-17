"""Project window"""
import dearpygui.dearpygui as dpg

from widget.swisscontrols.DataGrid import DataGrid
from widget.swisscontrols.ListEditCtrl import ListEditCtrl

from datasave import DataSave

from app.nodeeditor import NodeEditor

from components import Wire

class ProjectWindow:
    "Tab to edit the project"

    def __init__(self, name, close_project_tab):
        self.name = name
        self.save = DataSave(f"projects/{self.name}.json")

        with dpg.group(horizontal=True):
            with dpg.child_window(width=200, border=True, resizable_x=True):
                self.project_settings(close_project_tab)

                with dpg.tab_bar():
                    with dpg.tab(label="Wire"):
                        self.wire_editor()

            with dpg.tab_bar():
                with dpg.tab(label="Node editor",
                    drop_callback=self.part_drop, payload_type="part"):

                    NodeEditor(self.save)
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

    def wire_editor(self):
        "Wire editor"
        unsaved_grid_data = None

        # Load wire_grid
        wire_grid = DataGrid(
            title = "Wire editor",
            columns = ['', 'Color', 'Name', 'Gauge'],
            dtypes = [DataGrid.COLOR_CODE, DataGrid.COMBO, DataGrid.TXT_STRING, DataGrid.TXT_INT],
            defaults = [0, 0, "New wire", 20],
            combo_lists = [False, [key for key in Wire.str_to_color], False, False],
            data = self.save["wire"]
        )

        def save_change():
            nonlocal eval_grid
            self.save["wire"] = eval_grid.evaluate_grid().data

        # Editor grid
        wire_editor_id = dpg.generate_uuid()
        eval_grid = ListEditCtrl(wire_editor_id, save_change=save_change, grid=wire_grid)

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

    """def load_wires(self, wire_grid):
        for wire_name in self.save.get_children("wire"):
            wire = Wire(
                wire_name,
                self.save["wire", wire_name][0],
                self.save["wire", wire_name][1])

            wire_grid.append([(255, 255, 255, 255), False, wire.name, wire.gauge])

    def add_wire(self):
        name = dpg.get_value(f"{self.name}_input_name")
        color = dpg.get_value(f"{self.name}_color_list")
        gauge = dpg.get_value(f"{self.name}_input_awg")

        wire = Wire(name, color, gauge)

        status = self.save.check_tag_integrity(f"wire_{name}")
        dpg.set_value(f"{self.name}_wire_error_label", status)

        if status == "":
            self.save["wire", name] = (color, gauge)
            wire.add_to_table(self.name)"""

    def part_drop(self, sender, part):
        "Make nodes from draging part"
        # TODO : Implement fonction
