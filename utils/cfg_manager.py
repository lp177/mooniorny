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


def get_cfg(profil: str = "default") -> dict:

    cfg["ui"] = cfg_module_to_dict(profil, "ui")
    cfg["stocks"] = cfg_module_to_dict(profil, "stocks")
    cfg["alerts"] = cfg_module_to_dict(profil, "alerts")
    set_default_values(cfg)
    return cfg
