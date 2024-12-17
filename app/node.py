"""Node for the node editor"""
import dearpygui.dearpygui as dpg

from widget.swisscontrols.DataGrid import DataGrid
from widget.swisscontrols.ListEditCtrl import ListEditCtrl

from components import Wire

class Node:
    "Class representing a node"
    name = ""
    color = None
    node_type = ""
    position = ""
    lenght = 0

    wires: dict = dict()

    def __init__(self, parent, save,
            name, color, node_type, position, wires):
        self.parent = parent
        self.save = save

        self.save["node", name] = (color, node_type, position, wires)

        self.is_fliped = False

        with dpg.node(parent=parent,
            label=f"{self.save["node", name][1]} - {name}",
            user_data=name,
            pos=self.save["node", name][2],
            drop_callback=self.callback_wire_drop, payload_type="wire") as self.node_id:

            if node_type == "Cable":
                self.cable_attribute()
            elif node_type == "Part":
                self.part_attribute()

            with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Static):
                if self.save["wire"]:
                    wires = self.save["wire"][2]
                else:
                    wires = [""]

                wire_grid = DataGrid(
                    title="Wires",
                    columns = ['Wire'],
                    dtypes = [DataGrid.COMBO],
                    defaults = [False],
                    combo_lists = [wires],
                )

                wire_editor_id = dpg.generate_uuid()
                eval_grid = ListEditCtrl(wire_editor_id, grid=wire_grid, editable=False, width=100, height=100)

    @classmethod
    def from_json(cls, parent, name, save):
        "Create class from json"

        return cls(parent, save, name,
            save["node", name][0],
            save["node", name][1],
            save["node", name][2],
            save["node", name][3]
        )

    def data(self):
        "Class information without the name"
        return (self.color, self.node_type, self.position, self.wires)

    def part_attribute(self):
        "Attributes of the part node"

        def callback_flip_node(node_attribute):
            "Flip the input to the output"

            if self.is_fliped:
                dpg.configure_item(node_attribute,
                    user_data="OUT", attribute_type=dpg.mvNode_Attr_Output)
            else:
                dpg.configure_item(node_attribute,
                    user_data="IN", attribute_type=dpg.mvNode_Attr_Input)

            self.is_fliped = not self.is_fliped

        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Output) as self.attr_out:
            dpg.add_text("Connection")

        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Static):
            dpg.add_button(label="Flip", callback=lambda: callback_flip_node(self.attr_out))

            input_text = dpg.add_input_text(label="Part", width=150,
                        payload_type="part")

            with dpg.theme() as theme_error:
                with dpg.theme_component(dpg.mvAll):

                    dpg.add_theme_color(dpg.mvThemeCol_FrameBg,
                        (125, 50, 60), category=dpg.mvThemeCat_Core)

            dpg.bind_item_theme(input_text, theme_error)

    def cable_attribute(self):
        "Attributes of the cable node"

        with dpg.node_attribute(user_data="IN") as self.attr_in:
            dpg.add_text("In")

        with dpg.node_attribute(user_data="OUT",
                attribute_type=dpg.mvNode_Attr_Output) as self.attr_out:
            dpg.add_text("Out")

    def callback_wire_drop(self, _sender, wire):
        "Get when a wire is dropped on to the node"

        self.wires[wire.name] = wire.data()
        #status = self.save.update("node", self.name, self.data())

        #if status == "":
        #    self.add_wire(wire)
