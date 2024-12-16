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
            with dpg.child_window(width=200, border=True, resizable_x=True):
                self.project_settings(close_project_tab)

                with dpg.tab_bar():
                    with dpg.tab(label="Wire"):
                        self.wire_editor()

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

    def wire_editor(self):
        "Wire editor"
        unsaved_grid_data = None

        # Load wire_grid
        wire_grid = DataGrid(
            title="Wire editor",
            columns = ['', 'Color', 'Name', 'Gauge'],
            dtypes = [DataGrid.COLOR, DataGrid.COMBO, DataGrid.TXT_STRING, DataGrid.TXT_INT],
            defaults = [(255, 255, 255, 255), False, "New wire", 20],
            combo_lists = [None, [key for key in Wire.str_to_color], None, None],
            data=self.save["wire"]
        )

        def enable_editor():
            nonlocal unsaved_grid_data
            unsaved_grid_data = eval_grid.evaluate_grid().data

            dpg.disable_item(edit_button)

            dpg.enable_item(editing_buttons)
            dpg.enable_item(editor)

        def disable_editor():
            dpg.enable_item(edit_button)

            dpg.disable_item(editing_buttons)
            dpg.disable_item(editor)

        def cancel():
            nonlocal unsaved_grid_data

            eval_grid.set_grid_data(unsaved_grid_data)

            disable_editor()

        def save_change():
            self.save["wire"] = eval_grid.evaluate_grid().data

            disable_editor()

        dpg.add_text("", tag=f"{self.name}_wire_error_label", color=(250, 100, 120))

        # Edit, Cancel and Save buttons
        with dpg.group(horizontal=True):
            with dpg.group() as edit_button:
                dpg.add_button(label="Edit", callback=enable_editor)

            with dpg.group(horizontal=True, enabled=False) as editing_buttons:
                dpg.add_button(label="Cancel", callback=cancel)
                dpg.add_button(label="Save", callback=save_change)

        # Editor grid
        with dpg.group(enabled=False) as editor:
            wire_editor_id = dpg.generate_uuid()
            eval_grid = listEditCtrl(wire_editor_id, grid=wire_grid)

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
