"Class for the project manager"
import dearpygui.dearpygui as imgui

from datasave import DataSave

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
        self.save = DataSave("project_manager_save.txt", ["recent", "last_session"])

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
        imgui.add_listbox(items=[key for key in self.save["recent"]],
            tag="recent_project_list", num_items=10)

        imgui.add_button(label="Open", callback=self.open_recent_project)

        imgui.add_separator()

        # Create a new project
        imgui.add_text(tag="create_error_label", color=(250, 100, 120))

        imgui.add_input_text(label="name", source="create_project_name")
        imgui.add_button(label="Create project", callback=self.create_project)

    def open_last_session_project(self):
        "Open projects from last session"
        for project in self.save["last_session"]:
            self.open_project_tab(project)

    def open_recent_project(self):
        "Open a recent project"
        name = imgui.get_value("recent_project_list")

        if name in self.save.data["last_session"]:
            imgui.set_value("project_tab_bar", name)
            return

        self.open_project_tab(name)

    def create_project(self):
        "Create a new project"
        name = imgui.get_value("create_project_name")

        status = self.save.update("recent", name, None)

        imgui.set_value("create_error_label", status)

        if status == "":
            imgui.configure_item("recent_project_list",
                items=[key for key in self.save["recent"]])

            self.open_project_tab(name)

    def open_project_tab(self, name):
        "Once a project is created or opened, open it in a new tab"
        self.save.update("last_session", name, None)

        with imgui.tab(label=name, tag=name, parent="project_tab_bar"):
            ProjectWindow(name, self.close_project_tab)

        # Put the current tab to the open project
        imgui.set_value("project_tab_bar", name)

        # TODO : Close the menu bar

    def close_project_tab(self, _sender, _app_data, name):
        "Close project tab"

        self.save.remove("last_session", name)
        imgui.delete_item(name)
