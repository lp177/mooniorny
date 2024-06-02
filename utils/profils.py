import os, re, shutil
import dearpygui.dearpygui as dpg
from utils.modal import modal


cfg = {}


def cfg_module_to_dict(profil: str, section: str) -> dict:
    return getattr(
        getattr(__import__(f"profils.{profil}.{section}"), profil), section
    ).__dict__["cfg"]


def init_stock(stock: dict):
    if "colors" not in stock:
        stock["colors"] = {"default": cfg["ui"]["colors"]["default"]}
    elif "default" not in stock["colors"]:
        stock["colors"]["default"] = cfg["ui"]["colors"]["default"]
    if "name" not in stock:
        if "ISIN" not in stock:
            print("Invalide stock cfg: ", stock)
            return
        stock["name"] = stock["ISIN"]
    if "last_state" not in stock:
        stock["last_state"] = None


def set_default_values():

    for stock in cfg["stocks"]:
        init_stock(stock)


def get_profils_list() -> list:
    return [
        fs_item.path.replace("profils/", "")
        for fs_item in os.scandir("profils")
        if fs_item.is_dir()
    ]


def switch_profil(profil: str = "default") -> dict:
    from utils.plots import (
        clear_price_history,
        initialize_price_history,
        render_plots,
        monitor_stocks,
        delete_plots,
    )
    from components.menu.top_bar import create_profils_menu

    delete_plots()
    open_profil(profil)
    clear_price_history()
    initialize_price_history()
    render_plots()
    create_profils_menu()
    monitor_stocks()


def remove_profil(r):
    try:
        is_valid_profil_name(cfg["profil"]["current"])
        shutil.rmtree(f"profils/{cfg['profil']['current']}")
    except Exception as error_message:
        return modal(
            f"Fail to remove profil {cfg['profil']['current']}\n{error_message}",
            color=(250, 0, 0),
        )
    switch_profil("empty")


def error(error, display_error=False):
    if display_error:
        print(error)
    else:
        modal(error, color=(250, 0, 0))


def open_profil(profil: str = None, display_error=False) -> dict:

    if profil is None:
        from profils import session

        profil = session.cfg["last_profil_used"]
        if not is_valid_profil_name(profil, display_error):
            error(f"profil {profil} is invalide", display_error)
            profil = "empty"
        elif not os.path.isdir(f"profils/{profil}"):
            error(f"profil {profil} not found", display_error)
            profil = "empty"

    is_valid_profil_name(profil, display_error)
    cfg["profil"] = {"current": profil}
    try:
        cfg["ui"] = cfg_module_to_dict(profil, "ui")
        cfg["stocks"] = cfg_module_to_dict(profil, "stocks")
        cfg["alerts"] = cfg_module_to_dict(profil, "alerts")
    except Exception as error_message:
        if display_error:
            return modal(
                f"Fail to load profil {profil}\n{error_message}", color=(250, 0, 0)
            )
        raise Exception(f"Fail to load profil {profil}\n{error_message}")
    set_default_values()
    with open("profils/session.py", "w") as session_file:
        session_file.write('cfg = {"last_profil_used": "' + profil + '"}\n')
    return cfg


def create_profil(profil: str, copy_from_profil: str = "empty"):
    try:
        is_valid_profil_name(profil)
        is_valid_profil_name(copy_from_profil)
        shutil.copytree("profils/" + copy_from_profil, "profils/" + profil)
        switch_profil(profil)
        if dpg.does_item_exist("new_profil_window"):
            dpg.delete_item("new_profil_window")
    except Exception as error_message:
        print(error_message)
        if dpg.does_item_exist("new_profil_window_error"):
            dpg.delete_item("new_profil_window_error")
        dpg.add_text(
            str(error_message),
            color=(255, 0, 0),
            tag="new_profil_window_error",
            parent="new_profil_window",
            wrap=240,
        )


def is_valid_profil_name(profil: str, display_error=False):
    if not re.search(r"^[a-zA-Z0-9_]{1,100}$", profil):
        if display_error:
            modal(
                "Invalid profil name, syntax accepted is: 1 to 100 letters numbers and _",
                color=(250, 0, 0),
            )
            return False
        raise Exception(
            "Invalid profil name, syntax accepted is: 1 to 100 letters numbers and _"
        )
    return True
