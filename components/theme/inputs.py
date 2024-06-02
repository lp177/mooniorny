import dearpygui.dearpygui as dpg


def large_input():

    with dpg.theme() as large_input:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_style(
                dpg.mvStyleVar_FramePadding, x=10, y=10, category=dpg.mvThemeCat_Core
            )

    return large_input
