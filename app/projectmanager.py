"Class for the project manager"
import datetime

import dearpygui.dearpygui as imgui

from savefile import SaveFile

from app.projectwindow import ProjectWindow

#def callback(sender, app_data):
#    print('OK was clicked.')
#    print("Sender: ", sender)
#    print("App Data: ", app_data)

#def cancel_callback(sender, app_data):
#    print('Cancel was clicked.')
#    print("Sender: ", sender)
#    print("App Data: ", app_data)

class ProjectManager:
    "Project Manager menu"

    def __init__(self):
        self.recent_project_save = SaveFile("recent_project.txt")
        self.last_session_project_save = SaveFile("last_session_project.txt")

        self.open_last_session_project()

        # Import project from the file explorer
        #imgui.add_file_dialog(
        #    show=False, callback=callback, tag="file_dialog_id",
        #    cancel_callback=cancel_callback, width=700 ,height=400)

        #imgui.add_button(label="Import project",
        # callback=lambda: imgui.show_item("file_dialog_id"))

        #imgui.add_separator()

        # Select a project from recent ones
        imgui.add_text("Recent project")
        imgui.add_listbox(items=self.recent_project_save.data,
            tag="recent_project_list", num_items=10)

        imgui.add_button(label="Open", callback=self.open_recent_project)

        imgui.add_separator()

        # Create a new project
        imgui.add_text(tag="create_error_label", color=(250, 100, 120))

        imgui.add_input_text(label="name", source="create_project_name")
        imgui.add_button(label="Create project", callback=self.create_project)

    def open_last_session_project(self):
        "Open projects from last session"

        for project in self.last_session_project_save.data:
            self.open_project_tab(project)

    def open_recent_project(self):
        "Open a recent project"
        name = imgui.get_value("recent_project_list")

        if name in self.last_session_project_save.data:
            imgui.set_value("project_tab_bar", name)
            return

        self.last_session_project_save.append(name)
        self.open_project_tab(name)

    def create_project(self):
        "Create a new project"
        name = imgui.get_value("create_project_name")
        if name == "":
            imgui.set_value("create_error_label", "Enter a name with at least one character")
        elif self.recent_project_save.append(name):
            imgui.set_value("create_error_label", "")

            self.last_session_project_save.append(name)
            imgui.configure_item("recent_project_list", items=self.recent_project_save.data)
            self.open_project_tab(name)
        else:
            imgui.set_value("create_error_label", "Enter a different name than the other projects")

    def open_project_tab(self, name):
        "Once a project is created or opened, open it in a new tab"

        with imgui.tab(label=name, tag=name, parent="project_tab_bar"):
            ProjectWindow(name, self.close_project_tab)

        # Put the current tab to the open project
        imgui.set_value("project_tab_bar", name)

        # TODO : Close the menu bar

    def close_project_tab(self, sender, app_data, name):
        self.last_session_project_save.remove(name)
        imgui.delete_item(name)
