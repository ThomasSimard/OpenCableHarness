"""Node for the node editor"""
from abc import ABC, abstractmethod

import dearpygui.dearpygui as dpg

from widget.swisscontrols.DataGrid import DataGrid
from widget.swisscontrols.ListEditCtrl import ListEditCtrl

from datasave import DataSave

class Node(ABC):
    "Abstract node class"
    save: DataSave = None

    def __init__(self, parent, name, color, position):
        self.name = name

        Node.update_data(self.name, color, position, self.get_type())

        with dpg.node(parent=parent,
            label=f"{self.get_type()} - {self.name}",
            user_data=name,
            pos=self.position) as self.node_id:

            self.attribute()

    @classmethod
    def from_json(cls, parent, name):
        "Create abstract class from json"

        return cls(parent, name,
            Node.save["node", name][0],
            Node.save["node", name][1],
        )

    @staticmethod
    def update_data(name, color, position, node_type):
        "Update node data with its name"
        Node.save["node", name] = (color, position, node_type)

    @staticmethod
    def get_data(name):
        "Get node data with its name"
        return Node.save["node", name]

    @property
    def color(self):
        "Get node color"
        return Node.save["node", self.name][0]

    @property
    def position(self):
        "Get node position"
        return Node.save["node", self.name][1]

    @staticmethod
    @abstractmethod
    def get_type() -> str:
        "Node type"

    @abstractmethod
    def attribute(self):
        "Node attributes"

    @abstractmethod
    def get_attribute_in(self):
        "Get node attributes in"

    @abstractmethod
    def get_attribute_out(self):
        "Get node attributes out"

    @staticmethod
    def wire_attribute():
        "Node attribute to modify which wire is connected to it"
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Static):
            if Node.save["wire"]:
                wires = Node.save["wire"][2]
            else:
                wires = [""]

            wire_grid = DataGrid(
                title="Wires",
                columns = ['Wire'],
                dtypes = [DataGrid.COMBO],
                defaults = [False],
                combo_lists = [["lol"]],
            )

            wire_id = dpg.generate_uuid()
            return ListEditCtrl(wire_id, grid=wire_grid, force_save=False, width=130, height=100)

class Cable(Node):
    "Cable node"

    @staticmethod
    def get_type() -> str:
        return "Cable"

    def get_attribute_in(self):
        "Get attribute in"
        return self.attr_in

    def get_attribute_out(self):
        "Get attribute out"
        return self.attr_out

    def attribute(self):
        # Two attributes on the same line
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Static):
            dpg.add_spacer(width=100)

        with dpg.node_attribute(user_data="IN") as self.attr_in:
            dpg.bind_item_theme(dpg.last_item(), "theme_no_padding")

        with dpg.node_attribute(user_data="OUT",
                attribute_type=dpg.mvNode_Attr_Output) as self.attr_out:
            dpg.bind_item_theme(dpg.last_item(), "theme_no_padding")

        Node.wire_attribute()

class Part(Node):
    "Part node"
    library_save: DataSave = None

    @staticmethod
    def get_type() -> str:
        return "Part"

    def get_attribute_in(self):
        "Get attribute in"
        return self.attr

    def get_attribute_out(self):
        "Get attribute out"
        return self.attr

    @property
    def flipped(self):
        "Get if node is flipped"
        return Node.save["node-part", self.name, "flipped"]

    @flipped.setter
    def flipped(self, flipped):
        "Set if node is flipped"
        Node.save["node-part", self.name, "flipped"] = flipped

    def attribute(self):
        "Attributes of the part node"

        def apply_flip_attribute():
            if self.flipped:
                dpg.configure_item(self.attr,
                    user_data="OUT", attribute_type=dpg.mvNode_Attr_Output)
            else:
                dpg.configure_item(self.attr,
                    user_data="IN", attribute_type=dpg.mvNode_Attr_Input)

        def callback_flip_node():
            "Flip the input to the output"
            self.flipped = not self.flipped

            apply_flip_attribute()

        with dpg.node_attribute(user_data="OUT", attribute_type=dpg.mvNode_Attr_Output) as self.attr:
            dpg.add_spacer(width=100)

        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Static):
            dpg.add_button(label="Flip", callback=callback_flip_node)

            dpg.add_combo(items=[0,1], width=100, label="Part")

        apply_flip_attribute()

        Node.wire_attribute()
