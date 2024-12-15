"""Project manager window"""
import dearpygui.dearpygui as imgui

from app.projectmanager import ProjectManager
from app.partmanager import PartManager

class MainWindow:
    """Let the user create and open projects"""

    def __init__(self):
        with imgui.value_registry():
            imgui.add_string_value(tag="create_project_name")

        with imgui.window(label="Project Manager", tag="primary_window"):
            with imgui.tab_bar(tag="project_tab_bar", reorderable=True):
                pass

            with imgui.menu_bar():
                with imgui.menu(label="Project manager", tag="project_menu"):
                    ProjectManager()

                #with imgui.menu(label="Part library"):
                    #PartManager()

                with imgui.menu(label="Help"):
                    pass
