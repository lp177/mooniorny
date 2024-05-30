import dearpygui.dearpygui as dpg
from utils.modal import modal
from utils.plots_manager import (
    render_plots,
    update_graph,
    monitor_stocks,
    change_period,
)


def init_menu(_cfg: dict):
    global cfg
    cfg = _cfg
    modal(label="Settings", tag="settings_window", height=250, show=False)
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
    )
    dpg.add_text("Plot default width:")
    dpg.add_input_int(
        default_value=cfg["ui"]["graph_initial_width"],
        callback=update_plot_width,
    )
    dpg.add_text("Plot default time range:")
    dpg.add_combo(
        default_value=cfg["ui"]["default_time_range"],
        items=list(cfg["ui"]["periods"].keys()),
        callback=update_plot_time_range,
        width=100,
    )
    dpg.pop_container_stack()

    with dpg.viewport_menu_bar():
        with dpg.menu(label="File"):
            dpg.add_menu_item(label="Open dashboard", callback=work_in_progress)
            dpg.add_menu_item(label="Save dashboard", callback=work_in_progress)
            dpg.add_menu_item(label="Save dashboard as", callback=work_in_progress)
            with dpg.menu(label="Copy to clipboard"):
                dpg.add_menu_item(label="Image of dashboard", callback=work_in_progress)
                dpg.add_menu_item(label="Stock list", callback=work_in_progress)

        with dpg.menu(label="Preferences"):
            dpg.add_menu_item(
                label="UI",
                callback=lambda: dpg.configure_item("settings_window", show=True),
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


def sort_stocks_by_maturity(cfg: dict, state: str = "mature", reverse: bool = False):
    cfg["stocks"].sort(key=lambda stock: stock["state"] == state)
    render_plots(cfg)
    for stock in cfg["stocks"]:
        update_graph(cfg, stock)


def sort_stocks_by_name(cfg: dict, reverse: bool = False):
    cfg["stocks"].sort(key=lambda stock: stock["name"].upper())
    render_plots(cfg)
    for stock in cfg["stocks"]:
        update_graph(cfg, stock)


def monitor_on_off():
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


def update_plot_width(sender, app_data: int):
    cfg["ui"]["graph_initial_width"] = app_data
    render_plots(cfg)
    for stock in cfg["stocks"]:
        update_graph(cfg, stock)


def update_plot_time_range(sender, period: str):
    for stock in cfg["stocks"]:
        change_period(None, period, {"cfg": cfg, "stock": stock})


def work_in_progress():
    modal("work in progress", label="Not yet")


def show_help():
    modal("StockMonit version: 24.0521.1", label="About")
