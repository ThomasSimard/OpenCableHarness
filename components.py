"Cable class"

import json

import dearpygui.dearpygui as imgui

class Wire:
    "Class representing a wire"
    name = ""
    color = ""
    gauge = ""

    str_to_color = {
        "Black": (0, 0, 0, 255),
        "Red": (255, 0, 0, 255),
        "White": (255, 255, 255, 255),
        "Blue": (0, 0, 255, 255),
        "Green": (0, 255, 0, 255)
    }

    def __init__(self, name, color, gauge):
        self.name = name
        self.color = color
        self.gauge = gauge

    def data(self):
        "Put the object in json format"
        return (self.color, self.gauge)

    def __str__(self):
        return f"Wire : {self.name}, color : {self.color}, {self.gauge} awg"

    def show(self):
        "Standalone representation of a wire"
        with imgui.group(horizontal=True):
            imgui.add_color_button(default_value=Wire.str_to_color[self.color])
            imgui.add_text(self.name)
            imgui.add_text(f"{self.gauge} awg")

    @staticmethod
    def table_header(table_name):
        "Table header for the representation of a wire"
        with imgui.table(tag=f"{table_name}_wire_table", width=180):
            imgui.add_table_column(label="Color", width=25, width_fixed=True)
            imgui.add_table_column(label="Name")
            imgui.add_table_column(label="Awg", width=25, width_fixed=True)
            imgui.add_table_column(label="", width=25, width_fixed=True)

    def add_to_table(self, table_name):
        "Add wire to the table"
        with imgui.table_row(parent=f"{table_name}_wire_table"):
            imgui.add_color_button(default_value=Wire.str_to_color[self.color])

            text = imgui.add_text(self.name)

            imgui.add_text(self.gauge)

            with imgui.drag_payload(parent=text,
                drag_data=self,
                payload_type="wire"):

                self.show()

class Connector:
    "Class representing a connector"
    name = ""
    number_of_pins = 0

    def __init__(self, name, number_of_pins):
        self.name = name
        self.name = number_of_pins
