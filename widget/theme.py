"Put all the themes in this file"
import dearpygui.dearpygui as dpg

class Theme:
    "Put all the useful themes in here"

    def __init__(self):
        with dpg.theme(tag="theme_no_padding"):
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 0, 0)
                dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 0, 0)

        with dpg.theme(tag="theme_error"):
            with dpg.theme_component(dpg.mvAll):

                dpg.add_theme_color(dpg.mvThemeCol_FrameBg,
                    (125, 50, 60), category=dpg.mvThemeCat_Core)
