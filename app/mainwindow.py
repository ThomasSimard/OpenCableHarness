"""Project manager window"""
import dearpygui.dearpygui as dpg

from app.projectmanager import ProjectManager
from app.partmanager import PartManager

class MainWindow:
    """Let the user create and open projects"""

    def __init__(self):
        with dpg.value_registry():
            dpg.add_string_value(tag="create_project_name")

        with dpg.window(label="Project Manager", tag="primary_window"):
            with dpg.tab_bar(tag="project_tab_bar", reorderable=True):
                pass

            with dpg.menu_bar():
                with dpg.menu(label="Project manager", tag="project_menu"):
                    ProjectManager()

                #with dpg.menu(label="Part library"):
                    #PartManager()

                with dpg.menu(label="Help"):
                    pass
