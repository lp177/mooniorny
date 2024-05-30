def get_screen_height():
    import tkinter

    root = tkinter.Tk()
    height = root.winfo_screenheight()
    root.destroy()
    del tkinter
    return height


cfg = {
    "title": "Mooniorny",
    "monitor": True,
    "refresh_interval": 60,
    "default_time_range": "3 mois",
    "graph_initial_height": 345,
    "graph_initial_width": 420,
    "periods": {
        "All": "max",
        "10 ans": "10y",
        "5 ans": "5y",
        "2 ans": "2y",
        "1 an": "1y",
        "6 mois": "6mo",
        "3 mois": "3mo",
        "1 mois": "1mo",
        "5 jours": "5d",
        "1 jour": "1d",
    },
    "screen_height": get_screen_height() - 30,
    "screen_width": 2560,
    "default_maturity": "down",
    "colors": {
        "default": "226666",
        "maturity": "FFD700",
        "black": "000000",
        "blue": "226666",
        "green": "2D882D",
        "orange": "AA7939",
        "red": "801515",
        "white": "ffffff",
        "purple": "4F2C73",
        "yellow": "FFE800",
    },
}
