"""Editor section of the project window"""

import dearpygui.dearpygui as imgui

class NodeEditor:
    "Editor section"

    node_list = [0, 1, 2]

    def __init__(self, name):
        self.name = name

        with imgui.handler_registry():
            imgui.add_mouse_click_handler(button=1, callback=self.popup)

        with imgui.node_editor(tag=f"{self.name}_node_editor",
            callback=self.link_nodes, delink_callback=self.delink_nodes):

            for node in self.node_list:
                with imgui.node(label=f"Node: {node}"):
                    for i in range(1,3):
                        with imgui.node_attribute(shape=imgui.mvNode_PinShape_TriangleFilled):
                            imgui.add_input_text(label=f"cable {i}", width=150)
                        with imgui.node_attribute(shape=imgui.mvNode_PinShape_TriangleFilled,
                            attribute_type=imgui.mvNode_Attr_Output):

                            imgui.add_input_text(label=f"cable {i}", width=150)

    def add_node(self):
        "Add node to editor"
        name = imgui.get_value("popup_node_name")

        self.node_list.append(name)

        with imgui.node(label=f"Node: {name}", pos=imgui.get_mouse_pos(local=False),
            parent=f"{self.name}_node_editor"):

            for i in range(1,3):
                with imgui.node_attribute(shape=imgui.mvNode_PinShape_TriangleFilled):
                    imgui.add_input_text(label=f"cable {i}", width=150)
                with imgui.node_attribute(shape=imgui.mvNode_PinShape_TriangleFilled,
                    attribute_type=imgui.mvNode_Attr_Output):

                    imgui.add_input_text(label=f"cable {i}", width=150)

        self.delete_popup()

    def delete_popup(self):
        "Delete popup window"
        imgui.delete_item("popup")

    def node_popup(self, node):
        "Popup when clicked on a node"
        with imgui.window(tag="popup", modal=True, pos=imgui.get_mouse_pos(local=False),
            no_resize=True, no_collapse=True, label="Edit node", on_close=self.delete_popup):

            imgui.add_text("Node 1")
            imgui.add_input_text(label="Name", width=150)
            imgui.add_input_int(label="Number of pins", width=150)

            with imgui.group(horizontal=True):
                imgui.add_button(label="Edit")
                imgui.add_button(label="Delete")
                imgui.add_button(label="Cancel", callback=self.delete_popup)

    def node_editor_popup(self):
        "Popup when clicked on the node editor"
        with imgui.window(tag="popup", modal=True, pos=imgui.get_mouse_pos(local=False),
            no_resize=True, no_collapse=True, label="Add node", on_close=self.delete_popup):

            imgui.add_input_text(label="Name", tag="popup_node_name", width=150)

            with imgui.group(horizontal=True):
                imgui.add_button(label="Add", callback=self.add_node)
                imgui.add_button(label="Cancel", callback=self.delete_popup)

    def popup(self):
        "Popup menu when user right click"

        if imgui.is_item_hovered(f"{self.name}_node_editor"):
            hovered_node = None
            for node in imgui.get_item_children(f"{self.name}_node_editor", slot=1):
                if imgui.is_item_hovered(node):
                    hovered_node = node

            if hovered_node:
                self.node_popup(hovered_node)
            else:
                self.node_editor_popup()

    def link_nodes(self, sender, data):
        "Runs when node connect attributes"
        imgui.add_node_link(parent=sender, attr_1=data[0], attr_2=data[1])

    def delink_nodes(self, _, data):
        "Runs when node disconnect attributes"
        imgui.delete_item(data)
