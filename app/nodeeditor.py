"""Editor section of the project window"""

import dearpygui.dearpygui as dpg

from app.node import Node

class NodeEditor:
    "Editor section"

    def __init__(self, name, save):
        self.name = name
        self.save = save

        with dpg.handler_registry():
            dpg.add_mouse_click_handler(button=1, callback=self.popup)

        with dpg.node_editor(tag=f"{self.name}_node_editor", minimap=True,
            minimap_location=1, callback=self.link_nodes, delink_callback=self.delink_nodes):

            with dpg.node(label="Home node", draggable=False):
                with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Static):
                    dpg.add_text("Refference node!")

            # Load nodes from save file
            for node in self.save.get_children("node"):
                node = Node.from_json(f"{self.name}_node_editor", node, self.save)

    def add_node(self, _sender, _data, pos):
        "Add node to editor"
        # Arguments
        node_type = dpg.get_value("node_type")
        node_name = dpg.get_value("popup_node_name")
        node_color = dpg.get_value("popup_node_color")

        # Position
        ref_node = dpg.get_item_children(f"{self.name}_node_editor", slot=1)[0]

        ref_screen_pos = dpg.get_item_rect_min(ref_node)
        ref_grid_pos = dpg.get_item_pos(ref_node)

        pos[0] = pos[0] - (ref_screen_pos[0] - 8) + ref_grid_pos[0]
        pos[1] = pos[1] - (ref_screen_pos[1] - 8) + ref_grid_pos[1]

        # Create node
        node = Node(self.name,
            node_name, node_color,
            node_type, pos, dict())

        self.save["node", node_name] = node.data()

        self.delete_popup()

    def delete_popup(self):
        "Delete popup window"
        dpg.delete_item("popup")

    def delete_node(self, node):
        "Delete node"
        print('hello')
        #self.node_list.remove(node)

        dpg.delete_item(node)

    def node_popup(self, node):
        "Popup when clicked on a node"
        with dpg.window(tag="popup", modal=True, pos=dpg.get_mouse_pos(local=False),
            no_resize=True, no_collapse=True, label="Edit node", on_close=self.delete_popup):

            dpg.add_text("Node 1")
            dpg.add_input_text(label="Name", width=150)

            with dpg.group(horizontal=True):
                dpg.add_button(label="Edit")
                dpg.add_button(label="Delete")
                dpg.add_button(label="Cancel", callback=self.delete_popup)

    def node_editor_popup(self):
        "Popup when clicked on the node editor"
        with dpg.window(tag="popup", modal=True, pos=dpg.get_mouse_pos(local=False),
            no_resize=True, no_collapse=True,
            label="Add node", on_close=self.delete_popup):

            dpg.add_input_text(label="Name", tag="popup_node_name",
                default_value=f"X{len(self.save.get_children("node"))}", width=150)

            dpg.add_text("Type")
            dpg.add_radio_button(items=["Cable", "Part"],
                tag="node_type", default_value="Cable")

            dpg.add_color_edit(label="Color", tag="popup_node_color", no_alpha=True)

            with dpg.group(horizontal=True):
                dpg.add_button(label="Add",
                    callback=self.add_node, user_data=dpg.get_mouse_pos(local=False))

                dpg.add_button(label="Cancel", callback=self.delete_popup)

    def popup(self):
        "Popup menu when user right click"

        if dpg.is_item_hovered(f"{self.name}_node_editor"):
            hovered_node = None
            for node in dpg.get_item_children(f"{self.name}_node_editor", slot=1):
                if dpg.is_item_hovered(node):
                    hovered_node = node

            if hovered_node:
                self.node_popup(hovered_node)
            else:
                self.node_editor_popup()

    def link_nodes(self, sender, data):
        "Runs when node connect attributes"
        dpg.add_node_link(parent=sender, attr_1=data[0], attr_2=data[1])

    def delink_nodes(self, _, data):
        "Runs when node disconnect attributes"
        dpg.delete_item(data)
