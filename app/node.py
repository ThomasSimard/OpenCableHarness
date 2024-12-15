"""Node for the node editor"""
import dearpygui.dearpygui as imgui

from components import Wire

class Node:
    "Class representing a node"
    name = ""
    color = None
    node_type = ""
    position = ""
    lenght = 0

    wires = dict()

    def __init__(self, parent,
            name, color, node_type, position, wires):
        self.parent = parent

        self.name = name
        self.color = color

        self.node_type = node_type
        self.position = position

        self.wires = wires

        self.is_fliped = False

        with imgui.node(label=f"{self.node_type} - {self.name}",
            tag=f"{self.parent}_node_{self.name}",
            pos=self.position,
            parent=f"{self.parent}_node_editor",
            drop_callback=self.callback_wire_drop, payload_type="wire"):

            if self.node_type == "Cable":
                self.cable_attribute()
            elif self.node_type == "Part":
                self.part_attribute()

            #Load wires
            for wire in wires:
                self.add_wire(Wire(wire, *wires[wire]))

    @classmethod
    def from_json(cls, parent, name, save):
        "Create class from json"

        return cls(parent, name,
            save["node", name][0],
            save["node", name][1],
            save["node", name][2],
            save["node", name][3])

    def data(self):
        "Class information without the name"
        return (self.color, self.node_type, self.position, self.wires)

    def part_attribute(self):
        "Attributes of the part node"
        with imgui.node_attribute(tag=f"{self.parent}_{self.name}_link",
            attribute_type=imgui.mvNode_Attr_Output):
            imgui.add_text("Connection")

        with imgui.node_attribute(attribute_type=imgui.mvNode_Attr_Static):
            imgui.add_button(label="Flip", callback=self.callback_flip_node)

            input_text = imgui.add_input_text(label="Part", width=150,
                        payload_type="part")

            with imgui.theme() as theme_error:
                with imgui.theme_component(imgui.mvAll):

                    imgui.add_theme_color(imgui.mvThemeCol_FrameBg,
                        (125, 50, 60), category=imgui.mvThemeCat_Core)

            imgui.bind_item_theme(input_text, theme_error)

            Wire.table_header(f"{self.parent}_node_{self.name}")

    def callback_flip_node(self):
        "Flip the input to the output"

        if self.is_fliped:
            imgui.configure_item(f"{self.name}_link", attribute_type=imgui.mvNode_Attr_Output)
        else:
            imgui.configure_item(f"{self.name}_link", attribute_type=imgui.mvNode_Attr_Input)

        self.is_fliped = not self.is_fliped

    def cable_attribute(self):
        "Attributes of the cable node"

        with imgui.node_attribute():
            imgui.add_text("In")

        with imgui.node_attribute(attribute_type=imgui.mvNode_Attr_Output):
            imgui.add_text("Out")

        with imgui.node_attribute(attribute_type=imgui.mvNode_Attr_Static):
            Wire.table_header(f"{self.parent}_node_{self.name}")

    def add_wire(self, wire):
        with imgui.node_attribute(parent=f"{self.parent}_node_{self.name}",
            attribute_type=imgui.mvNode_Attr_Static):

            wire.add_to_table(f"{self.parent}_node_{self.name}")

            #imgui.add_button(label="x", callback=self.remove_wire)

    def callback_remove_wire(self, sender):
        parent = imgui.get_item_parent(sender)
        wire = imgui.get_value(imgui.get_item_children(parent, slot=1)[1])

        self.wires.remove(wire)

        node_attribute = imgui.get_item_parent(parent)
        imgui.delete_item(node_attribute)

    def callback_wire_drop(self, _sender, wire):
        "Get when a wire is dropped on to the node"

        self.wires[wire.name] = wire.data()
        #status = self.save.update("node", self.name, self.data())

        #if status == "":
        #    self.add_wire(wire)
