import dearpygui.dearpygui as dpg

from widget.swisscontrols.DataGrid import DataGrid
from widget.swisscontrols.ListEditCtrl import ListEditCtrl

from datasave import DataSave

class PartManager:
    "Part Manager menu"

    def __init__(self):
        self.save = DataSave("part_manager.json")

        dpg.add_input_text(readonly=True)

        part_grid = DataGrid(
            title="Part library editor",
            columns = ['Manufacturer', 'Name', 'Pins'],
            dtypes = [DataGrid.COLOR, DataGrid.TXT_STRING, DataGrid.TXT_INT],
            defaults = [(255, 255, 255, 255), "New wire", 20],
            combo_lists = [None, None, None],
            data=self.save["part"]
        )

        # Editor grid
        grid_id = dpg.generate_uuid()
        eval_grid = ListEditCtrl(grid_id, grid=part_grid, width=200, height=200)

        """dpg.add_text("Add part")
        dpg.add_input_text(label="name", tag="part_name")

        dpg.add_text("Manufacturer list")
        #dpg.add_listbox(self.save.get_list("manufacturer"), tag="manufacturer_list")

        dpg.add_button(label="Select")

        dpg.add_input_text(label="manufacturer", tag="manufacturer_input_text")
        dpg.add_button(label="Add manufacturer",
            callback=self.update_manufacturer_save_file)

        dpg.add_input_int(label="pins", tag="connector_pin",
            default_value=1, min_value=1, min_clamped=True)

        dpg.add_input_text(label="image")

        dpg.add_button(label="Add", callback=self.add_part)

        dpg.add_separator()

        dpg.add_text("Part list")

        dpg.add_input_text(label="filter", tag="part_filter",
            callback=self.part_filter)

        dpg.add_listbox(self.save.get_children("part"),
            tag="part_list", num_items=20, callback=self.part_selected)

        with dpg.drag_payload(parent="part_list", tag="part_list_payload",
            drag_data=dpg.get_value("part_list"), payload_type="part"):

            dpg.add_text(dpg.get_value("part_list"), tag="part_list_payload_label")"""

    def part_selected(self, _, part):
        dpg.configure_item("part_list_payload", drag_data=part)
        dpg.set_value("part_list_payload_label", part)

    def add_part(self):
        "Add part to library"
        part_name = dpg.get_value("part_name")
        part_manufacturer = dpg.get_value("manufacturer_list")
        part_pin = dpg.get_value("connector_pin")

        status = self.save.check_tag_integrity(f"part_{part_name}")

        if status == "":
            self.save["part", part_name] = (part_manufacturer, part_pin)
            dpg.configure_item("part_list", items=self.save.get_children("part"))

    def update_manufacturer_save_file(self):
        "Update manufacturer save file with a callback"
        status = self.save.check_tag_integrity(f"manufacturer_{dpg.get_value("manufacturer_input_text")}")

        if status == "":
            self.save["manufacturer", dpg.get_value("manufacturer_input_text")] = True
            dpg.configure_item("manufacturer_list",
                items=self.save.get_children("manufacturer"))
