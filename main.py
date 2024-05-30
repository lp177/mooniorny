import time
import threading
from profils import session
import dearpygui.dearpygui as dpg
from utils.cfg_manager import get_cfg
from utils.plots_manager import render_plots, initialize_price_history, monitor_stocks
from components.menu.top_bar import init_menu


def initialize_gui(cfg):
    dpg.create_context()
    dpg.create_viewport(
        title=cfg["ui"]["title"],
        width=2560,
        height=cfg["ui"]["screen_height"],
        large_icon = "images/mooniorny.ico",
        small_icon = "images/mooniorny_small.ico"
    )
    dpg.set_viewport_small_icon("images/mooniorny_small.ico")
    dpg.set_viewport_large_icon("images/mooniorny.ico")
    render_plots(cfg)
    init_menu(cfg)
    dpg.setup_dearpygui()
    dpg.show_viewport()


def start_monitoring():
    while True:
        time.sleep(cfg["ui"]["refresh_interval"])
        if cfg["ui"]["monitor"] is True:
            monitor_stocks(cfg)


cfg = get_cfg(session.cfg["last_profil_used"])

initialize_price_history(cfg)
initialize_gui(cfg)
monitor_stocks(cfg)

thread = threading.Thread(target=start_monitoring)
thread.daemon = True
thread.start()

dpg.start_dearpygui()
dpg.destroy_context()
