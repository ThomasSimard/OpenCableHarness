"""Editor section of the project window"""

import dearpygui.dearpygui as dpg

from app.node import Node

from datasave import DataSave

class NodeEditor:
    "Editor section"

    def __init__(self, save: DataSave):
        self.save = save

        self.handlers()

        with dpg.node_editor(minimap=True,
            minimap_location=1,
            callback=self.link_nodes, delink_callback=self.delink_nodes) as self.editor_id:

            with dpg.node(label="Home node", draggable=False):
                with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Static):
                    dpg.add_text("Refference node!")

            nodes = {}

            # Load nodes from save file
            for node in self.save.get_children("node"):
                nodes[node] = Node.from_json(self.editor_id, node, self.save)

            # Load links from file
            for link in self.save.get_children("link"):
                node_names = link.split("_")

                node_in: Node = nodes[node_names[0]]
                node_out: Node = nodes[node_names[1]]

                if node_in.get_type() == "Part":
                    attr_in = node_in.attr
                else:
                    attr_in = node_in.attr_in

                if node_out.get_type() == "Part":
                    attr_out = node_out.attr
                else:
                    attr_out = node_out.attr_out

                dpg.add_node_link(user_data=(node_names[0], node_names[1]), attr_1=attr_in, attr_2=attr_out)

    def handlers(self):
        draging_node = None
        mouse_pos = None

        def left_click_handler():
            nonlocal draging_node
            nonlocal mouse_pos

            self.callback_close_popup()

            draging_node = self._node_hovered()
            mouse_pos = dpg.get_mouse_pos(local=False)

        def left_release_handler():
            nonlocal draging_node
            nonlocal mouse_pos

            if draging_node and mouse_pos != dpg.get_mouse_pos(local=False):
                name = dpg.get_item_user_data(draging_node)
                position = dpg.get_item_pos(draging_node)

                self.save["node", name] = (self.save["node", name][0],
                                           self.save["node", name][1],
                                           position,
                                           self.save["node", name][3])

        with dpg.handler_registry():
            dpg.add_mouse_click_handler(button=1, callback=self.popup)
            dpg.add_mouse_click_handler(button=0, callback=left_click_handler)
            dpg.add_mouse_release_handler(button=0, callback=left_release_handler)

    def _node_hovered(self):
        "Get if hover a node"
        for node in dpg.get_item_children(self.editor_id, slot=1):
            if dpg.is_item_hovered(node):
                return node

    def add_node(self, _sender, _data, pos):
        "Add node to editor"
        # Arguments
        node_type = dpg.get_value("node_type")
        node_name = dpg.get_value("popup_node_name")
        node_color = dpg.get_value("popup_node_color")

        # Position
        ref_node = dpg.get_item_children(self.editor_id, slot=1)[0]

        ref_screen_pos = dpg.get_item_rect_min(ref_node)
        ref_grid_pos = dpg.get_item_pos(ref_node)

        pos[0] = pos[0] - (ref_screen_pos[0] - 8) + ref_grid_pos[0]
        pos[1] = pos[1] - (ref_screen_pos[1] - 8) + ref_grid_pos[1]

        # Create node
        node = Node(self.editor_id, self.save,
            node_name, node_color,
            node_type, pos, dict())

        dpg.delete_item("popup")

    def callback_close_popup(self):
        "Close popup when left clicking off it"
        if dpg.does_item_exist("popup"):
            # Do not close the popup if you are hover it
            if dpg.is_item_hovered("popup"):
                return

            for children in dpg.get_item_children("popup", slot=1):
                if dpg.get_item_state(children).get("hovered"):
                    return

            dpg.delete_item("popup")

    def popup(self):
        "Popup menu when user right click"
        # Close popup if its already open
        if dpg.does_item_exist("popup"):
            dpg.delete_item("popup")

        # Return if not in node editor
        if not dpg.is_item_hovered(self.editor_id):
            return


        def add_node():
            # Clear selections
            dpg.clear_selected_nodes(self.editor_id)
            dpg.clear_selected_links(self.editor_id)

            dpg.delete_item("popup")

            with dpg.window(tag="popup", modal=True, pos=dpg.get_mouse_pos(local=False),
                no_resize=True, no_collapse=True,
                label="Add node"):

                dpg.add_input_text(label="Name", tag="popup_node_name",
                    default_value=f"X{len(self.save.get_children("node"))}", width=150)

                dpg.add_text("Type")
                dpg.add_radio_button(items=["Cable", "Part"],
                    tag="node_type", default_value="Cable")

                dpg.add_color_edit(label="Color", tag="popup_node_color", no_alpha=True)

                with dpg.group(horizontal=True):
                    dpg.add_button(label="Add",
                        callback=self.add_node, user_data=dpg.get_mouse_pos(local=False))

                    dpg.add_button(label="Cancel", callback=lambda: dpg.delete_item("popup"))

        def edit_node():
            # Clear selections
            dpg.clear_selected_nodes(self.editor_id)
            dpg.clear_selected_links(self.editor_id)

            dpg.delete_item("popup")

            with dpg.window(tag="popup", modal=True, pos=dpg.get_mouse_pos(local=False),
                no_resize=True, no_collapse=True, label="Edit node"):

                dpg.add_text("Node 1")
                dpg.add_input_text(label="Name", width=150)

                with dpg.group(horizontal=True):
                    dpg.add_button(label="Edit")
                    dpg.add_button(label="Delete")
                    dpg.add_button(label="Cancel", callback=lambda: dpg.delete_item("popup"))

        def unlink(links):
            for link in links:
                data = dpg.get_item_user_data(link)

                del self.save["link", str(data[0]), str(data[1])]

                dpg.delete_item(link)

            # Clear node slections
            dpg.clear_selected_nodes(self.editor_id)
            dpg.delete_item("popup")

        def delete_nodes(nodes):
            # TODO : Do you want to delete those nodes
            for node in nodes:
                name = dpg.get_item_user_data(node)
                del self.save["node", name]

                dpg.delete_item(node)

            dpg.delete_item("popup")

        # Get selected nodes and links
        nodes = dpg.get_selected_nodes(self.editor_id)
        links = dpg.get_selected_links(self.editor_id)

        # Popup menu
        with dpg.window(tag="popup", pos=dpg.get_mouse_pos(local=False),
                no_resize=True, no_move=True, no_title_bar=True, no_collapse=True,
                height=80,
                label="Add node"):

            dpg.add_menu_item(label="Add node", callback=add_node)

            if len(nodes) == 1:
                dpg.add_separator()
                dpg.add_menu_item(label="Edit node")

            if links:
                dpg.add_separator()
                dpg.add_menu_item(label="Unlink", callback=lambda: unlink(links))

            if nodes:
                dpg.add_menu_item(label="Delete nodes", callback=lambda: delete_nodes(nodes))

    def link_nodes(self, sender, data):
        "Runs when node connect attributes"
        node0 = dpg.get_item_user_data(dpg.get_item_parent(data[0]))
        node1 = dpg.get_item_user_data(dpg.get_item_parent(data[1]))

        if dpg.get_item_user_data(data[0]) == "IN":
            self.save["link", node0, node1] = True
            user_data = (dpg.get_item_user_data(dpg.get_item_parent(data[0])),
                       dpg.get_item_user_data(dpg.get_item_parent(data[1])))
        else:
            self.save["link", node1, node0] = True
            user_data = (dpg.get_item_user_data(dpg.get_item_parent(data[1])),
                       dpg.get_item_user_data(dpg.get_item_parent(data[0])))

        dpg.add_node_link(
            parent=sender,
            user_data=user_data,
            attr_1=data[0],
            attr_2=data[1]
        )

    def delink_nodes(self, _, data):
        "Runs when node are deleted so disconnect attributes"
        dpg.delete_item(data)
        del self.save["link", str(data[0]), str(data[1])]
