"""Editor section of the project window"""

import dearpygui.dearpygui as imgui

from components import Node

class NodeEditor:
    "Editor section"

    node_list = []

    def __init__(self, name):
        self.name = name

        with imgui.handler_registry():
            imgui.add_mouse_click_handler(button=1, callback=self.popup)

        with imgui.node_editor(tag=f"{self.name}_node_editor", minimap=True,
            minimap_location=1, callback=self.link_nodes, delink_callback=self.delink_nodes):

            pass

    def add_node(self):
        "Add node to editor"
        node = Node(imgui.get_value("popup_node_name"), imgui.get_value("popup_node_color"), None)

        self.node_list.append(node)

        with imgui.node(label=f"Node - {node.name}",
            tag=f"node_{node.name}",pos=imgui.get_mouse_pos(local=False),
            parent=f"{self.name}_node_editor") as node_id:

            with imgui.theme() as item_theme:
                with imgui.theme_component(imgui.mvAll):
                    node.color[3] = 100
                    imgui.add_theme_color(imgui.mvNodeCol_TitleBar,
                        node.color, category=imgui.mvThemeCat_Nodes)

                    node.color[3] = 150
                    imgui.add_theme_color(imgui.mvNodeCol_TitleBarHovered,
                        node.color, category=imgui.mvThemeCat_Nodes)

                    node.color[3] = 255
                    imgui.add_theme_color(imgui.mvNodeCol_TitleBarSelected,
                        node.color, category=imgui.mvThemeCat_Nodes)

                    # TODO : make node title easy to read with light color

            imgui.bind_item_theme(node_id, item_theme)

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

    def delete_node(self, node):
        "Delete node"
        print('hello')
        #self.node_list.remove(node)

        imgui.delete_item(node)

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
            no_resize=True, no_collapse=True, height=275,
            label="Add node", on_close=self.delete_popup):

            imgui.add_input_text(label="Name", tag="popup_node_name",
                default_value=f"X{len(self.node_list)}", width=150)

            imgui.add_color_picker(tag="popup_node_color",
                no_alpha=True, picker_mode=imgui.mvColorPicker_wheel)

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
