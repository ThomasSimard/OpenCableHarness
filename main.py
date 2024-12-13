"Main app"
import dearpygui.dearpygui as imgui

from app.mainwindow import MainWindow


def main():
    "Main fonction of the app"
    imgui.create_context()

    #imgui.show_documentation()
    #imgui.show_style_editor()
    #imgui.show_debug()
    #imgui.show_about()
    #imgui.show_metrics()
    #imgui.show_font_manager()
    #imgui.show_item_registry()

    imgui.create_viewport(title='Open Cable Harness',
        width=600, height=400, min_width=600, min_height=400)

    MainWindow()

    imgui.setup_dearpygui()
    imgui.show_viewport()

    imgui.set_primary_window("primary_window", True)

    imgui.start_dearpygui()

if __name__ == '__main__':
    try:
        main()
        imgui.destroy_context()
    except KeyboardInterrupt:
        imgui.destroy_context()
