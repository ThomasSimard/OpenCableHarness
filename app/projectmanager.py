"Class for the project manager"
import dearpygui.dearpygui as dpg

from datasave import DataSave

from app.projectwindow import ProjectWindow

class ProjectManager:
    "Project Manager menu"

    def __init__(self):
        self.save = DataSave("project_manager_save.json")

        self.open_last_session_project()

        # Import project from the file explorer
        # TODO Add this fonctionnality
        #dpg.add_file_dialog(
        #    show=False, callback=callback, tag="file_dialog_id",
        #    cancel_callback=cancel_callback, width=700 ,height=400)

        #dpg.add_button(label="Import project",
        # callback=lambda: dpg.show_item("file_dialog_id"))

        #dpg.add_separator()

        # Select a project from recent ones
        dpg.add_text("Recent project")
        dpg.add_listbox(items=self.save.get_children("recent"),
            tag="recent_project_list", num_items=10)

        dpg.add_menu_item(label="Open", callback=self.open_recent_project)

        dpg.add_separator()

        # Create a new project
        dpg.add_text(tag="create_error_label", color=(250, 100, 120))

        dpg.add_input_text(label="name", source="create_project_name")
        dpg.add_menu_item(label="Create project", callback=self.create_project)

    def open_last_session_project(self):
        "Open projects from last session"
        for project in self.save.get_children("last_session"):
            self.open_project_tab(project)

    def open_recent_project(self):
        "Open a recent project"
        name = dpg.get_value("recent_project_list")

        # Nothing selected
        if name == "":
            return

        if self.save["last_session", name]:
            dpg.set_value("project_tab_bar", name)
            return

        self.open_project_tab(name)

    def create_project(self):
        "Create a new project"
        name = dpg.get_value("create_project_name")

        status = self.save.check_tag_integrity(f"recent_{name}")
        dpg.set_value("create_error_label", status)

        if status == "":
            self.save["recent", name] = True

            dpg.configure_item("recent_project_list",
                items=self.save.get_children("recent"))

            self.open_project_tab(name)

    def open_project_tab(self, name):
        "Once a project is created or opened, open it in a new tab"
        # Reset text input
        dpg.set_value("create_project_name", "")

        # Save open tabs
        self.save["last_session", name] = True

        with dpg.tab(label=name, tag=name, parent="project_tab_bar"):
            ProjectWindow(name, self.close_project_tab)

        # Put the current tab to the open project
        dpg.set_value("project_tab_bar", name)

    def close_project_tab(self, _sender, _app_data, name):
        "Close project tab"

        del self.save["last_session", name]
        dpg.delete_item(name)
