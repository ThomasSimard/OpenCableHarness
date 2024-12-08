"""Project manager window"""
import time

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

    def __init__(self):
        self.recent_project_list=[]
        self.load_recent_project()

        with imgui.value_registry():
            imgui.add_string_value(tag="create_project_name")

        with imgui.window(label="Project Manager", tag="primary_window"):
            with imgui.menu_bar():
                with imgui.menu(label="Project", tag="project_menu"):
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

            with imgui.tab_bar(tag="project_tab_bar"):
                pass

    def update_recent_project(self, file_path):
        "Update the save list of recent projects to save file"

        if file_path not in self.recent_project_list:
            self.recent_project_list.append(file_path)

            with open("recent_project.txt", 'w', encoding='utf-8') as save_file:
                save_file.write(json.dumps(self.recent_project_list))

            imgui.configure_item("recent_project_list", items=self.recent_project_list)

            self.open_project_tab(file_path)

    def load_recent_project(self):
        """Load recent projects from the save file"""

        with open("recent_project.txt", 'r', encoding='utf-8') as save_file:
            try:
                self.recent_project_list = json.loads(save_file.read())
            except JSONDecodeError:
                pass

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
            self.update_recent_project(name)

    def open_project_tab(self, file_path):
        "Once a project is created or opened, open it in a new tab"

        with imgui.tab(label=file_path, tag=file_path, parent="project_tab_bar"):
            ProjectWindow()

        # Put the current tab to the open project
        imgui.set_value("project_tab_bar", file_path)

        # TODO : Close the menu bar
