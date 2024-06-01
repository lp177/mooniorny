import os, re, shutil
import dearpygui.dearpygui as dpg
from utils.modal import modal


cfg = {}


def cfg_module_to_dict(profil: str, section: str) -> dict:
    return getattr(
        getattr(__import__(f"profils.{profil}.{section}"), profil), section
    ).__dict__["cfg"]


def init_stock(cfg: dict, stock: dict):
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


def set_default_values(cfg: dict):

    for stock in cfg["stocks"]:
        init_stock(cfg, stock)


def get_profils_list() -> list:
    return [ fs_item.path.replace("profils/", "") for fs_item in os.scandir("profils") if fs_item.is_dir() ]

def open_profil(profil: str = "default") -> dict:

    is_valid_profil_name(profil)
    cfg["ui"] = cfg_module_to_dict(profil, "ui")
    cfg["stocks"] = cfg_module_to_dict(profil, "stocks")
    cfg["alerts"] = cfg_module_to_dict(profil, "alerts")
    set_default_values(cfg)
    return cfg


def init_profil(profil: str, copy_from_profil: str = "empty"):
    try:
        is_valid_profil_name(profil)
        is_valid_profil_name(copy_from_profil)
        shutil.copytree("profils/" + copy_from_profil, "profils/" + profil)
        open_profil(profil)
        if dpg.does_item_exist("new_profil_window"):
            dpg.delete_item("new_profil_window")
        from components.menu import create_profils_menu
        create_profils_menu()
    except Exception as error_message:
        if dpg.does_item_exist("new_profil_window_error"):
            dpg.delete_item("new_profil_window_error")
        dpg.add_text(str(error_message), color=(255,0,0), tag="new_profil_window_error", parent="new_profil_window", wrap=240)

def is_valid_profil_name(profil: str):
    if not re.search(r"^[a-zA-Z0-9_]{1,100}$", profil):
        raise Exception("Invalid profil name, syntax accepted is: 1 to 100 letters numbers and _")
