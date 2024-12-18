"Main app"
import dearpygui.dearpygui as dpg

from app.mainwindow import MainWindow
from widget.theme import Theme

def main():
    "Main fonction of the app"

    dpg.create_context()

    Theme()

    #dpg.show_documentation()
    #dpg.show_style_editor()
    #dpg.show_debug()
    #dpg.show_about()
    #dpg.show_metrics()
    #dpg.show_font_manager()
    #dpg.show_item_registry()

    dpg.create_viewport(title='Open Cable Harness',
        width=800, height=600, min_width=800, min_height=600)

    MainWindow()

    dpg.setup_dearpygui()
    dpg.show_viewport()

    dpg.set_primary_window("primary_window", True)

    dpg.start_dearpygui()

if __name__ == '__main__':
    try:
        main()
        dpg.destroy_context()
    except KeyboardInterrupt:
        dpg.destroy_context()
