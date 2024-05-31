import dearpygui.dearpygui as dpg
from utils.modal import modal
from utils.plots_manager import (
    render_plots,
    update_graph,
    monitor_stocks,
    change_period,
)
import webbrowser

settings_windows = ["about_modal", "settings_window", "work_in_progress"]


def init_menu(_cfg: dict):
    global cfg
    cfg = _cfg

    with dpg.viewport_menu_bar():
        with dpg.menu(label="Dashboards"):
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
                label="Alphabetic", callback=lambda: sort_stocks_by_name(_cfg)
            )
            dpg.add_menu_item(label="Market", callback=work_in_progress)
            dpg.add_menu_item(
                label="Maturity", callback=lambda: sort_stocks_by_maturity(_cfg)
            )

        with dpg.menu(label="Monit"):
            dpg.add_menu_item(label="Refresh now", callback=lambda: monitor_stocks(cfg))
            dpg.add_menu_item(label="Pause", callback=monitor_on_off, check=True)

        dpg.add_menu_item(label="Help", callback=show_help)


def close_all_settings_windows():

    for tag in settings_windows:
        if dpg.does_item_exist(tag):
            dpg.delete_item(tag)


def create_settings_ui_window():
    close_all_settings_windows()
    modal(label="Settings", tag="settings_window", height=250)
    dpg.push_container_stack("settings_window")
    dpg.add_text("Set Refresh Interval (seconds):")
    dpg.add_input_int(
        default_value=cfg["ui"]["refresh_interval"],
        callback=update_refresh_interval,
    )
    dpg.add_text("Plot default height:")
    dpg.add_input_int(
        default_value=cfg["ui"]["graph_initial_height"],
        callback=update_plot_height,
        tag="input_plot_height",
    )
    dpg.add_text("Plot default width:")
    dpg.add_input_int(
        default_value=cfg["ui"]["graph_initial_width"],
        callback=update_plot_width,
        tag="input_plot_width",
    )
    dpg.add_text("Plot default time range:")
    dpg.add_combo(
        default_value=cfg["ui"]["default_time_range"],
        items=list(cfg["ui"]["periods"].keys()),
        callback=update_plot_time_range,
        width=100,
    )
    dpg.pop_container_stack()


def sort_stocks_by_maturity(cfg: dict, state: str = "mature", reverse: bool = False):
    close_all_settings_windows()
    cfg["stocks"].sort(key=lambda stock: stock["state"] == state)
    render_plots(cfg)
    for stock in cfg["stocks"]:
        update_graph(cfg, stock)


def sort_stocks_by_name(cfg: dict, reverse: bool = False):
    close_all_settings_windows()
    cfg["stocks"].sort(key=lambda stock: stock["name"].upper())
    render_plots(cfg)
    for stock in cfg["stocks"]:
        update_graph(cfg, stock)


def monitor_on_off():
    close_all_settings_windows()
    if cfg["ui"]["monitor"]:
        cfg["ui"]["monitor"] = not cfg["ui"]["monitor"]
        return
    cfg["ui"]["monitor"] = True
    monitor_stocks(cfg)


def update_refresh_interval(sender, app_data: int):
    cfg["ui"]["refresh_interval"] = app_data


def update_plot_height(sender, app_data: int):
    cfg["ui"]["graph_initial_height"] = app_data
    render_plots(cfg)
    for stock in cfg["stocks"]:
        update_graph(cfg, stock)
    dpg.focus_item("input_plot_height")


def update_plot_width(sender, app_data: int):
    cfg["ui"]["graph_initial_width"] = app_data
    render_plots(cfg)
    for stock in cfg["stocks"]:
        update_graph(cfg, stock)
    dpg.focus_item("input_plot_width")


def update_plot_time_range(sender, period: str):
    for stock in cfg["stocks"]:
        change_period(None, period, {"cfg": cfg, "stock": stock})


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
