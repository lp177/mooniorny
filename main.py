import time
import threading
from profils import session
import dearpygui.dearpygui as dpg
from utils.profils import cfg, open_profil
from utils.plots import render_plots, initialize_price_history, monitor_stocks
from components.menu.top_bar import init_menu
from components.shortcuts.keyboards_global import init_global_shortcuts


def initialize_gui():
    dpg.create_context()
    # init_global_shortcuts()
    dpg.create_viewport(
        title=cfg["ui"]["title"],
        width=2560,
        height=cfg["ui"]["screen_height"],
        large_icon="images/mooniorny.ico",
        small_icon="images/mooniorny_small.ico",
    )
    dpg.set_viewport_small_icon("images/mooniorny_small.ico")
    dpg.set_viewport_large_icon("images/mooniorny.ico")
    render_plots()
    init_menu()
    dpg.setup_dearpygui()
    dpg.show_viewport()


def start_monitoring():
    while True:
        time.sleep(cfg["ui"]["refresh_interval"])
        if cfg["ui"]["monitor"] is True:
            monitor_stocks()

open_profil(session.cfg["last_profil_used"])
initialize_price_history()
initialize_gui()
monitor_stocks()

thread = threading.Thread(target=start_monitoring)
thread.daemon = True
thread.start()

dpg.start_dearpygui()
dpg.destroy_context()
