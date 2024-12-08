"""Project manager window"""
import json
from json.decoder import JSONDecodeError

import dearpygui.dearpygui as imgui

from app.projectwindow import ProjectWindow

#def callback(sender, app_data):
#    print('OK was clicked.')
#    print("Sender: ", sender)
#    print("App Data: ", app_data)

#def cancel_callback(sender, app_data):
#    print('Cancel was clicked.')
#    print("Sender: ", sender)
#    print("App Data: ", app_data)

class MainWindow:
    """Let the user create and open projects"""

    data_path = "data/"
    recent_project_save_path = data_path + "recent_project.txt"
    manufacturer_save_path = data_path + "manufacturer.txt"

    def __init__(self):
        self.recent_project_list = self.load_save_file(self.recent_project_save_path)
        self.manufacturer_list = self.load_save_file(self.manufacturer_save_path)

        with imgui.value_registry():
            imgui.add_string_value(tag="create_project_name")

        with imgui.window(label="Project Manager", tag="primary_window"):
            with imgui.menu_bar():
                with imgui.menu(label="Project manager", tag="project_menu"):
                    # TODO : do not let user open twice the same project

                    # Import project from the file explorer
                    #imgui.add_file_dialog(
                    #    show=False, callback=callback, tag="file_dialog_id",
                    #    cancel_callback=cancel_callback, width=700 ,height=400)

                    #imgui.add_button(label="Import project",
                    # callback=lambda: imgui.show_item("file_dialog_id"))

                    #imgui.add_separator()

                    # Select a project from recent ones
                    if self.recent_project_list:
                        imgui.add_text("Recent project")
                        imgui.add_listbox(items=self.recent_project_list,
                            tag="recent_project_list", num_items=10)

                        imgui.add_button(label="Open", callback=self.open_recent_project)
                    else:
                        imgui.add_text("No recent project!")

                    imgui.add_separator()

                    # Create a new project
                    imgui.add_text(tag="create_error_label", color=(250, 100, 120))

                    imgui.add_input_text(label="name", source="create_project_name")
                    imgui.add_button(label="Create project", callback=self.create_project)

                with imgui.menu(label="Part library"):
                    imgui.add_text("Add part")
                    imgui.add_input_text(label="name")

                    imgui.add_text("Manufacturer list")
                    imgui.add_listbox(self.manufacturer_list, tag="manufacturer_list")

                    imgui.add_button(label="Select")

                    imgui.add_input_text(label="manufacturer", tag="manufacturer_input_text")
                    imgui.add_button(label="Add manufacturer",
                        callback=self.update_manufacturer_save_file)

                    imgui.add_input_int(label="pins",
                        default_value=1, min_value=1, min_clamped=True)

                    imgui.add_input_text(label="image")

                    imgui.add_button(label="Add")

                    imgui.add_separator()

                    imgui.add_text("Part list")
                    imgui.add_input_text(label="search")
                    imgui.add_listbox([1, 2, 3, 4], num_items=20)

            with imgui.tab_bar(tag="project_tab_bar"):
                pass

    def update_save_file(self, new_data, data_list, save_file, tag):
        "Update the save list of recent projects to save file"

        if new_data not in data_list:
            data_list.append(new_data)

            with open(save_file, 'w', encoding='utf-8') as file:
                file.write(json.dumps(data_list))

            imgui.configure_item(tag, items=data_list)

            return True

        return False

    def update_manufacturer_save_file(self):
        "Update manufacturer save file with a callback"
        self.update_save_file(imgui.get_value("manufacturer_input_text"),
            self.manufacturer_list, self.manufacturer_save_path, "manufacturer_list")

    def load_save_file(self, save_file):
        """Load recent projects from the save file"""

        try:
            with open(save_file, 'r', encoding='utf-8') as save_file:
                try:
                    return json.loads(save_file.read())
                except JSONDecodeError:
                    return []
        except FileNotFoundError:
            return []

    def open_recent_project(self):
        "Open a recent project"
        self.open_project_tab(imgui.get_value("recent_project_list"))

    def create_project(self):
        "Create a new project"
        name = imgui.get_value("create_project_name")
        if name == "":
            imgui.set_value("create_error_label", "Enter a name with at least one character")
        elif name in self.recent_project_list:
            imgui.set_value("create_error_label", "Enter a different name than the other projects")
        else:
            if self.update_save_file(name, self.recent_project_list, self.recent_project_save_path, "recent_project_list"):
                self.open_project_tab(name)

    def open_project_tab(self, file_path):
        "Once a project is created or opened, open it in a new tab"

        with imgui.tab(label=file_path, tag=file_path, parent="project_tab_bar"):
            ProjectWindow()

        # Put the current tab to the open project
        imgui.set_value("project_tab_bar", file_path)

        # TODO : Close the menu bar
