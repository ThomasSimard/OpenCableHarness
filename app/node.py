"""Node for the node editor"""

import dearpygui.dearpygui as imgui

from components import Wire

class Node:
    "Class representing a node"
    name = ""
    color = None
    part = None

    def __init__(self, name, color, part):
        self.name = name
        self.color = color
        self.part = part

class PartNode:
    "Part node"

    def __init__(self, name):
        self.parent = f"node_{name}"

        with imgui.node_attribute():
            imgui.add_text("Connection")

        with imgui.node_attribute(attribute_type=imgui.mvNode_Attr_Output):
            imgui.add_text("Out")

        with imgui.node_attribute(attribute_type=imgui.mvNode_Attr_Static):
            imgui.add_button(label="Flip")

            input_text = imgui.add_input_text(label="Part", width=150,
                        payload_type="part")

            with imgui.theme() as theme_error:
                with imgui.theme_component(imgui.mvAll):

                    imgui.add_theme_color(imgui.mvThemeCol_FrameBg,
                        (125, 50, 60), category=imgui.mvThemeCat_Core)

        imgui.bind_item_theme(input_text, theme_error)


class CableNode:
    "Cable node"
    wire_list = []

    def __init__(self, name):
        self.parent = f"node_{name}"
        imgui.configure_item(self.parent, drop_callback=self.drop, payload_type="wire")

        with imgui.node_attribute():
            imgui.add_text("In")

        with imgui.node_attribute(attribute_type=imgui.mvNode_Attr_Output):
            imgui.add_text("Out")

        with imgui.node_attribute(attribute_type=imgui.mvNode_Attr_Static):
            Wire.table_header(f"node_{name}")

    def add_wire(self, wire):
        if wire not in self.wire_list:
            self.wire_list.append(wire)

            with imgui.node_attribute(parent=self.parent,
                attribute_type=imgui.mvNode_Attr_Static):

                wire.add_to_table(self.parent)

                #imgui.add_button(label="x", callback=self.remove_wire)

    def remove_wire(self, sender):
        parent = imgui.get_item_parent(sender)
        wire = imgui.get_value(imgui.get_item_children(parent, slot=1)[1])

        self.wire_list.remove(wire)

        node_attribute = imgui.get_item_parent(parent)
        imgui.delete_item(node_attribute)

    def drop(self, sender, wire):
        self.add_wire(wire)
