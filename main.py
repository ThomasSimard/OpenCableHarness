"Main app"
import dearpygui.dearpygui as imgui

from app.mainwindow import MainWindow

def main():
    "Main fonction of the app"
    imgui.create_context()
    imgui.create_viewport(title='Open Cable Harness', width=600, height=400, min_width=600, min_height=400)

    MainWindow()

    imgui.setup_dearpygui()
    imgui.show_viewport()

    imgui.set_primary_window("primary_window", True)

    imgui.start_dearpygui()
    imgui.destroy_context()

if __name__ == '__main__':
    main()
