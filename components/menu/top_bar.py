import dearpygui.dearpygui as dpg
from utils.modal import modal
from utils.image import insert_image
from components.theme.loader import get_theme
from utils.profils import (
    cfg,
    get_profils_list,
    create_profil,
    switch_profil,
    remove_profil,
)
from utils.plots import (
    render_plots,
    update_graph,
    monitor_stocks,
    change_period,
)
import webbrowser

settings_windows = [
    "about_modal",
    "new_profil_window",
    "settings_window",
    "work_in_progress",
]


def init_menu():

    with dpg.viewport_menu_bar():
        create_profils_menu()
        with dpg.menu(label="Dashboards", tag="dashboards_menu"):
            dpg.add_menu_item(label="New dashboard", callback=work_in_progress)
            dpg.add_menu_item(label="Open dashboard", callback=work_in_progress)
            dpg.add_menu_item(label="Save dashboard", callback=work_in_progress)
            dpg.add_menu_item(label="Save dashboard as", callback=work_in_progress)
            with dpg.menu(label="Clipboard"):
                dpg.add_menu_item(
                    label="Copy image of dashboard", callback=work_in_progress
                )
                dpg.add_menu_item(
                    label="Copy dashboard settings", callback=work_in_progress
                )
                dpg.add_menu_item(
                    label="Past dashboard settings", callback=work_in_progress
                )

        with dpg.menu(label="Settings"):
            dpg.add_menu_item(
                label="UI",
                callback=create_settings_ui_window,
            )
            dpg.add_menu_item(label="Stocks", callback=work_in_progress)
            dpg.add_menu_item(label="Alerts", callback=work_in_progress)

        with dpg.menu(label="Sort"):
            dpg.add_menu_item(
                label="Alphabetic", callback=lambda: sort_stocks_by_name()
            )
            dpg.add_menu_item(label="Market", callback=work_in_progress)
            dpg.add_menu_item(
                label="Maturity", callback=lambda: sort_stocks_by_maturity()
            )

        with dpg.menu(label="Monit"):
            dpg.add_menu_item(label="Refresh now", callback=lambda: monitor_stocks())
            dpg.add_menu_item(label="Pause", callback=monitor_on_off, check=True)

        dpg.add_menu_item(label="Help", callback=show_help)


def create_profils_menu():
    if dpg.does_item_exist("profils_menu"):
        dpg.delete_item("profils_menu")
        before = "dashboards_menu"
    else:
        before = 0
    with dpg.menu(label="Profils", tag="profils_menu", before=before):
        dpg.add_menu_item(label="New profil", callback=create_new_profil_window)
        dpg.add_menu_item(label="Save profil", callback=work_in_progress)
        dpg.add_menu_item(label="Delete profil", callback=remove_profil)
        with dpg.menu(label="Open profil"):
            profils = get_profils_list()
            for profil in profils:
                if profil == "empty":
                    continue
                dpg.add_menu_item(
                    label=profil,
                    callback=lambda sender, state, profil: switch_profil(profil),
                    user_data=profil,
                    check=True,
                    default_value=profil == cfg["profil"]["current"],
                )


def close_all_settings_windows():

    for tag in settings_windows:
        if dpg.does_item_exist(tag):
            dpg.delete_item(tag)


def create_new_profil_window():
    close_all_settings_windows()
    modal(label="Profils", tag="new_profil_window", height=250)
    large_input_theme = get_theme("inputs", "large_input")
    dpg.push_container_stack("new_profil_window")
    dpg.add_text("New profil name:")
    dpg.add_input_text(
        tag="new_profil_name",
        on_enter=True,
        callback=lambda: create_profil(
            dpg.get_value("new_profil_name"), dpg.get_value("new_profil_copy_from")
        ),
    )
    dpg.bind_item_theme("new_profil_name", large_input_theme)
    dpg.add_text("Copy from:")
    dpg.add_combo(
        default_value="empty",
        items=get_profils_list(),
        tag="new_profil_copy_from",
    )
    dpg.bind_item_theme("new_profil_copy_from", large_input_theme)
    dpg.add_dummy(height=10)
    dpg.add_button(
        label="Create",
        callback=lambda: create_profil(
            dpg.get_value("new_profil_name"), dpg.get_value("new_profil_copy_from")
        ),
        indent=60,
        tag="create_new_profil_bt",
    )
    dpg.bind_item_theme("create_new_profil_bt", large_input_theme)
    dpg.pop_container_stack()


def create_settings_ui_window():
    close_all_settings_windows()
    modal(label="Settings", tag="settings_window", height=300)
    dpg.push_container_stack("settings_window")
    dpg.add_text("Set Refresh Interval (seconds):")
    insert_image(image_path="images/save.png", texture_tag="save", just_texture=True)
    large_input_theme = get_theme("inputs", "large_input")
    with dpg.group(horizontal=True):
        dpg.add_input_int(
            default_value=cfg["ui"]["refresh_interval"],
            tag="update_refresh_interval_input",
        )
        dpg.bind_item_theme("update_refresh_interval_input", large_input_theme)
        dpg.add_image_button(
            texture_tag="save", width=27, height=27, callback=update_refresh_interval
        )
    dpg.add_text("Plot default height:")
    with dpg.group(horizontal=True):
        dpg.add_input_int(
            default_value=cfg["ui"]["graph_initial_height"],
            tag="input_plot_height",
        )
        dpg.bind_item_theme("input_plot_height", large_input_theme)
        dpg.add_image_button(
            texture_tag="save", width=27, height=27, callback=update_plot_height
        )
    dpg.add_text("Plot default width:")
    with dpg.group(horizontal=True):
        dpg.add_input_int(
            default_value=cfg["ui"]["graph_initial_width"],
            tag="input_plot_width",
        )
        dpg.bind_item_theme("input_plot_width", large_input_theme)
        dpg.add_image_button(
            texture_tag="save", width=27, height=27, callback=update_plot_width
        )
    dpg.add_text("Plot default time range:")
    dpg.add_combo(
        default_value=cfg["ui"]["default_time_range"],
        items=list(cfg["ui"]["periods"].keys()),
        width=100,
        callback=update_plot_time_range,
        tag="input_plot_time_range",
    )
    dpg.bind_item_theme("input_plot_time_range", large_input_theme)
    dpg.pop_container_stack()


def sort_stocks_by_maturity(state: str = "mature", reverse: bool = False):
    close_all_settings_windows()
    cfg["stocks"].sort(key=lambda stock: stock["state"] == state)
    render_plots()
    for stock in cfg["stocks"]:
        update_graph(stock)


def sort_stocks_by_name(reverse: bool = False):
    close_all_settings_windows()
    cfg["stocks"].sort(key=lambda stock: stock["name"].upper())
    render_plots()
    for stock in cfg["stocks"]:
        update_graph(stock)


def monitor_on_off():
    close_all_settings_windows()
    if cfg["ui"]["monitor"]:
        cfg["ui"]["monitor"] = not cfg["ui"]["monitor"]
        return
    cfg["ui"]["monitor"] = True
    monitor_stocks()


def update_refresh_interval():
    cfg["ui"]["refresh_interval"] = dpg.get_value("update_refresh_interval_input")


def update_plot_height():
    cfg["ui"]["graph_initial_height"] = dpg.get_value("input_plot_height")
    render_plots()
    for stock in cfg["stocks"]:
        update_graph(stock)
    dpg.focus_item("input_plot_height")


def update_plot_width():
    cfg["ui"]["graph_initial_width"] = dpg.get_value("input_plot_width")
    render_plots()
    for stock in cfg["stocks"]:
        update_graph(stock)
    dpg.focus_item("input_plot_width")


def update_plot_time_range(sender, period: str):
    for stock in cfg["stocks"]:
        change_period(None, period, {"stock": stock})


def work_in_progress():
    close_all_settings_windows()
    modal("work in progress", label="Not yet", tag="work_in_progress")


def show_help():
    close_all_settings_windows()
    modal("StockMonit version: 24.0521.1", label="About", tag="about_modal")
    dpg.push_container_stack("about_modal")
    dpg.add_button(
        label="https://github.com/lp177/mooniorny",
        callback=lambda: webbrowser.open("https://github.com/lp177/mooniorny"),
    )
    dpg.pop_container_stack()
