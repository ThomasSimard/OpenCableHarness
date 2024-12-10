"""Node for the node editor"""

import dearpygui.dearpygui as imgui

class Node:
    "Class representing a node"
    name = ""
    color = None
    part = None

    def __init__(self, name, color, part):
        self.name = name
        self.color = color
        self.part = part

class CableNode:
    wire_list = []

    def __init__(self, name):
        self.parent = f"node_{name}"

        with imgui.node_attribute():
            imgui.add_text("In")

        with imgui.node_attribute(attribute_type=imgui.mvNode_Attr_Output):
            imgui.add_text("Out")

        with imgui.node_attribute(attribute_type=imgui.mvNode_Attr_Static):
            imgui.add_button(label="Add wire", callback=self.add_wire)

    def add_wire(self, wire=""):
        self.wire_list.append(wire)

        with imgui.node_attribute(parent=self.parent,
            attribute_type=imgui.mvNode_Attr_Static):

            with imgui.group(horizontal=True):
                input_text = imgui.add_input_text(width=150,
                    callback=self.text_changed,
                    drop_callback=self.drop, payload_type="wire")

                with imgui.theme() as theme_error:
                    with imgui.theme_component(imgui.mvAll):

                        imgui.add_theme_color(imgui.mvThemeCol_FrameBg,
                            (125, 50, 60), category=imgui.mvThemeCat_Core)

                imgui.bind_item_theme(input_text, theme_error)

                #imgui.add_button(label="x", callback=self.remove_wire)

    def text_changed(self, sender, value):
        print(value)

    def remove_wire(self, sender):
        parent = imgui.get_item_parent(sender)
        wire = imgui.get_value(imgui.get_item_children(parent, slot=1)[1])

        self.wire_list.remove(wire)

        node_attribute = imgui.get_item_parent(parent)
        imgui.delete_item(node_attribute)

    def drop(self, sender, wire):
        imgui.set_value(sender, wire)
