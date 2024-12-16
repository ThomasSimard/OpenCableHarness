"""Node for the node editor"""
import dearpygui.dearpygui as dpg

from components import Wire

class Node:
    "Class representing a node"
    name = ""
    color = None
    node_type = ""
    position = ""
    lenght = 0

    wires: dict = dict()

    def __init__(self, parent,
            name, color, node_type, position, wires):
        self.parent = parent

        self.name = name
        self.color = color

        self.node_type = node_type
        self.position = position

        self.wires = wires

        self.is_fliped = False

        with dpg.node(label=f"{self.node_type} - {self.name}",
            pos=self.position,
            parent=self.parent,
            drop_callback=self.callback_wire_drop, payload_type="wire") as self.node_id:

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

        def callback_flip_node(node_attribute):
            "Flip the input to the output"

            if self.is_fliped:
                dpg.configure_item(node_attribute, attribute_type=dpg.mvNode_Attr_Output)
            else:
                dpg.configure_item(node_attribute, attribute_type=dpg.mvNode_Attr_Input)

            self.is_fliped = not self.is_fliped

        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Output) as node_attribute:
            dpg.add_text("Connection")

        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Static):
            dpg.add_button(label="Flip", callback=lambda: callback_flip_node(node_attribute))

            input_text = dpg.add_input_text(label="Part", width=150,
                        payload_type="part")

            with dpg.theme() as theme_error:
                with dpg.theme_component(dpg.mvAll):

                    dpg.add_theme_color(dpg.mvThemeCol_FrameBg,
                        (125, 50, 60), category=dpg.mvThemeCat_Core)

            dpg.bind_item_theme(input_text, theme_error)

            Wire.table_header(f"{self.parent}_node_{self.name}")

    def cable_attribute(self):
        "Attributes of the cable node"

        with dpg.node_attribute():
            dpg.add_text("In")

        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Output):
            dpg.add_text("Out")

        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Static):
            Wire.table_header(f"{self.parent}_node_{self.name}")

    def add_wire(self, wire):
        with dpg.node_attribute(parent=f"{self.parent}_node_{self.name}",
            attribute_type=dpg.mvNode_Attr_Static):

            wire.add_to_table(f"{self.parent}_node_{self.name}")

            #dpg.add_button(label="x", callback=self.remove_wire)

    def callback_remove_wire(self, sender):
        parent = dpg.get_item_parent(sender)
        wire = dpg.get_value(dpg.get_item_children(parent, slot=1)[1])

        self.wires.remove(wire)

        node_attribute = dpg.get_item_parent(parent)
        dpg.delete_item(node_attribute)

    def callback_wire_drop(self, _sender, wire):
        "Get when a wire is dropped on to the node"

        self.wires[wire.name] = wire.data()
        #status = self.save.update("node", self.name, self.data())

        #if status == "":
        #    self.add_wire(wire)
