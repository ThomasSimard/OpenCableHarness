"""Project window"""

import dearpygui.dearpygui as imgui

class CreateWindow:
    "Create pop up for new nodes"

    def __init__(self):
        ""
        #title_label = tk.Label(root, text="Create new")
        #title_label.grid()

        #name_label = tk.Label(root, text="Name:")
        #name_label.grid(row=1, column=0)

        #self.cable_name_entry = tk.Entry(root)
        #self.cable_name_entry.grid(row=1, column=1)

        #pin_label = tk.Label(root, text="Number of pins:")
        #pin_label.grid(row=2, column=0)

        #self.pin_combobox = ttk.Combobox(root, values=["1", "2", "3", "4", "5", "6", "7", "8"])
        #self.pin_combobox.grid(row=2, column=1)

        #create_button = tk.Button(root, text="Create")
        #create_button.grid(row=3, column=0, columnspan=2)

class ProjectWindow:
    "Tab to edit the project"

    cable_list = []
    node_list = []

    def __init__(self):
        with imgui.node_editor(callback=self.link_callback, delink_callback=self.delink_callback):
            with imgui.node(label="Node 1"):
                with imgui.node_attribute(label="Node A1"):
                    imgui.add_input_float(label="F1", width=150)

                with imgui.node_attribute(label="Node A2", attribute_type=imgui.mvNode_Attr_Output):
                    imgui.add_input_float(label="F2", width=150)

            with imgui.node(label="Node 2"):
                with imgui.node_attribute(label="Node A3"):
                    imgui.add_input_float(label="F3", width=200)

                with imgui.node_attribute(label="Node A4", attribute_type=imgui.mvNode_Attr_Output):
                    imgui.add_input_float(label="F4", width=200)

    def link_callback(self, sender, app_data):
        "Runs when node connect attributes"
        # app_data -> (link_id1, link_id2)
        imgui.add_node_link(app_data[0], app_data[1], parent=sender)

    def delink_callback(self, sender, app_data):
        "Runs when node disconnect attributes"
        # app_data -> link_id
        imgui.delete_item(app_data)

    def open_create_new_window(self):
        "Open the create new window"
        #CreateWindow()
