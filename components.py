"Cable class"

import json

import dearpygui.dearpygui as dpg

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
        with dpg.group(horizontal=True):
            dpg.add_color_button(default_value=Wire.str_to_color[self.color])
            dpg.add_text(self.name)
            dpg.add_text(f"{self.gauge} awg")

class Connector:
    "Class representing a connector"
    name = ""
    number_of_pins = 0

    def __init__(self, name, number_of_pins):
        self.name = name
        self.name = number_of_pins
