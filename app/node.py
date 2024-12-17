"""Node for the node editor"""
import dearpygui.dearpygui as dpg

from widget.swisscontrols.DataGrid import DataGrid
from widget.swisscontrols.ListEditCtrl import ListEditCtrl

from components import Wire

class Node:
    "Class representing a node"
    COLOR = 0
    TYPE = 1
    POSITION = 2
    WIRES = 3

    def __init__(self, parent, save,
            name, color, node_type, position, wires):
        self.parent = parent
        self.save = save

        self.name = name
        self.save["node", name] = (color, node_type, position, wires)

        with dpg.node(parent=parent,
            label=f"{self.save["node", name][Node.TYPE]} - {name}",
            user_data=name,
            pos=self.save["node", name][Node.POSITION],
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

                editor_id = dpg.generate_uuid()
                eval_grid = ListEditCtrl(editor_id, grid=wire_grid, editable=False, width=100, height=100)

    def get_type(self):
        return self.save["node", self.name][Node.TYPE]

    @classmethod
    def from_json(cls, parent, name, save):
        "Create class from json"

        return cls(parent, save, name,
            save["node", name][Node.COLOR],
            save["node", name][Node.TYPE],
            save["node", name][Node.POSITION],
            save["node", name][Node.WIRES]
        )

    def part_attribute(self):
        "Attributes of the part node"

        def apply_flip_attribute(flipped):
            if flipped:
                dpg.configure_item(self.attr,
                    user_data="OUT", attribute_type=dpg.mvNode_Attr_Output)
            else:
                dpg.configure_item(self.attr,
                    user_data="IN", attribute_type=dpg.mvNode_Attr_Input)

        def callback_flip_node():
            "Flip the input to the output"
            self.save["node-part", self.name, "flipped"] = not self.save["node-part", self.name, "flipped"]

            apply_flip_attribute(self.save["node-part", self.name, "flipped"])

        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Output) as self.attr:
            dpg.add_text("Connection")

        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Static):
            dpg.add_button(label="Flip", callback=callback_flip_node)

            input_text = dpg.add_input_text(label="Part", width=150,
                        payload_type="part")

            with dpg.theme() as theme_error:
                with dpg.theme_component(dpg.mvAll):

                    dpg.add_theme_color(dpg.mvThemeCol_FrameBg,
                        (125, 50, 60), category=dpg.mvThemeCat_Core)

            dpg.bind_item_theme(input_text, theme_error)

        apply_flip_attribute(self.save["node-part", self.name, "flipped"])

    def cable_attribute(self):
        "Attributes of the cable node"

        with dpg.node_attribute(user_data="IN") as self.attr_in:
            dpg.add_text("In")

        with dpg.node_attribute(user_data="OUT",
                attribute_type=dpg.mvNode_Attr_Output) as self.attr_out:
            dpg.add_text("Out")

    def callback_wire_drop(self, _sender, wire):
        "Get when a wire is dropped on to the node"
        # TODO implement
        #self.wires[wire.name] = wire.data()
        #status = self.save.update("node", self.name, self.data())

        #if status == "":
        #    self.add_wire(wire)
