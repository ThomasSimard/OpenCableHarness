import dearpygui.dearpygui as imgui

from datasave import DataSave

class PartManager:
    def __init__(self):
        self.save = DataSave("part_manager.json", ["manufacturer", "part"])

        imgui.add_text("Add part")
        imgui.add_input_text(label="name", tag="part_name")

        imgui.add_text("Manufacturer list")
        imgui.add_listbox(self.save.get_list("manufacturer"), tag="manufacturer_list")

        imgui.add_button(label="Select")

        imgui.add_input_text(label="manufacturer", tag="manufacturer_input_text")
        imgui.add_button(label="Add manufacturer",
            callback=self.update_manufacturer_save_file)

        imgui.add_input_int(label="pins", tag="connector_pin",
            default_value=1, min_value=1, min_clamped=True)

        imgui.add_input_text(label="image")

        imgui.add_button(label="Add", callback=self.add_part)

        imgui.add_separator()

        imgui.add_text("Part list")

        imgui.add_input_text(label="filter", tag="part_filter",
            callback=self.part_filter)

        imgui.add_listbox(self.save.get_list("part"),
            tag="part_list", num_items=20, callback=self.part_selected)

        with imgui.drag_payload(parent="part_list", tag="part_list_payload",
            drag_data=imgui.get_value("part_list"), payload_type="part"):

            imgui.add_text(imgui.get_value("part_list"), tag="part_list_payload_label")

    def part_filter(self, sender, value):
        "Update listbox filter"

    def part_selected(self, _, part):
        imgui.configure_item("part_list_payload", drag_data=part)
        imgui.set_value("part_list_payload_label", part)

    def add_part(self):
        "Add part to library"
        part_name = imgui.get_value("part_name")
        part_manufacturer = imgui.get_value("manufacturer_list")
        part_pin = imgui.get_value("connector_pin")

        status = self.save.update("part", part_name, (part_manufacturer, part_pin))

        if status == "":
            imgui.configure_item("part_list", items=self.save.get_list("part"))

    def update_manufacturer_save_file(self):
        "Update manufacturer save file with a callback"
        status = self.save.update("manufacturer", imgui.get_value("manufacturer_input_text"), None)

        if status == "":
            imgui.configure_item("manufacturer_list",
                items=self.save.get_list("manufacturer"))
