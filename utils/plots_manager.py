import yfinance, datetime
import dearpygui.dearpygui as dpg
from utils.notify import alert


plot_lines_tags = {}
plot_line_themes = {}
previous_prices = {}
price_history = {}
date_history = {}
maturities = {}


def initialize_price_history(cfg: dict):
    for stock in cfg["stocks"]:
        ticker = yfinance.Ticker(stock["ISIN"])
        history = ticker.history(
            period=cfg["ui"]["periods"][cfg["ui"]["default_time_range"]],
            repair=True,
            prepost=True,
        )
        price_history[stock["ISIN"]] = history["Close"].tolist()
        date_history[stock["ISIN"]] = [
            int(date.timestamp()) for date in history.index.tolist()
        ]
        previous_prices[stock["ISIN"]] = price_history[stock["ISIN"]][-1]


def monitor_stocks(cfg: dict):
    for stock in cfg["stocks"]:
        ticker = yfinance.Ticker(stock["ISIN"])
        last_day_history = ticker.history(
            period="1d",
            repair=True,
            prepost=True,
        )
        last_price = last_day_history["Close"].iloc[-1]
        previous_prices[stock["ISIN"]] = last_price
        price_history[stock["ISIN"]].append(last_price)
        date_history[stock["ISIN"]].append(int(last_day_history.index[-1].timestamp()))

        update_graph(cfg, stock)


def apply_line_color_to(cfg: dict, to: str, color: str):
    if color in cfg["ui"]["colors"]:
        color = cfg["ui"]["colors"][color]
    if color not in plot_line_themes:
        with dpg.theme() as plot_theme:
            with dpg.theme_component(dpg.mvLineSeries):
                dpg.add_theme_color(
                    dpg.mvPlotCol_Line,
                    tuple(int(color[i : i + 2], 16) for i in (0, 2, 4)),
                    category=dpg.mvThemeCat_Plots,
                )
        plot_line_themes[color] = plot_theme
    dpg.bind_item_theme(to, plot_line_themes[color])


price_condition_function = {
    "up": lambda price, up: price >= up,
    "down": lambda price, down: price <= down,
}


def update_graph(cfg: dict, stock: dict):

    default_color = stock["colors"]["default"]
    segments = []
    current_segment = {"color": default_color, "points": []}

    if "price_condition" not in stock["colors"]:
        apply_line_color_to(cfg, f"Plot_{stock['ISIN']}", default_color)
        dpg.set_value(
            f"Plot_{stock['ISIN']}",
            [date_history[stock["ISIN"]], price_history[stock["ISIN"]]],
        )
        dpg.fit_axis_data(f"{stock['ISIN']}_x_axis")
        dpg.fit_axis_data(f"{stock['ISIN']}_y_axis")
        return

    state = None
    maturity = (
        stock["maturity"] if "maturity" in stock else cfg["ui"]["default_maturity"]
    )
    maturity_color = (
        stock["colors"]["maturity"]
        if "maturity" in stock["colors"]
        else cfg["ui"]["colors"]["maturity"]
    )
    for i in range(len(price_history[stock["ISIN"]])):
        price = price_history[stock["ISIN"]][i]
        date = date_history[stock["ISIN"]][i]

        color = default_color
        for color_name, condition in stock["colors"]["price_condition"].items():
            if price_condition_function[condition["feature"]](
                price, condition["value"]
            ):
                if maturity is not None and condition["feature"] == maturity:
                    color = maturity_color
                    state = "mature"
                else:
                    color = color_name
                    state = condition["feature"]
                break
            else:
                state = None

        if color != current_segment["color"]:
            if current_segment["points"]:
                segments.append(current_segment)
                current_segment = {
                    "color": color,
                    "points": [current_segment["points"][-1]],
                }
            else:
                current_segment = {"color": color, "points": []}

        current_segment["points"].append((date, price))

    stock["state"] = state
    if state == "maturity":
        if stock["name"] not in maturities:
            maturities[stock["name"]] = datetime.datetime.now()
            alert(cfg, stock["name"], price)
    elif stock["name"] in maturities:
        if maturities[stock["name"]] > datetime.datetime.now() - datetime.timedelta(
            minutes=15
        ):
            del maturities[stock["name"]]

    if current_segment["points"]:
        segments.append(current_segment)

    i = 0
    if stock["ISIN"] in plot_lines_tags:
        for tag in plot_lines_tags[stock["ISIN"]]:
            dpg.delete_item(tag)
    plot_lines_tags[stock["ISIN"]] = []
    for segment in segments:
        tag = f"{stock['ISIN']}_y_axis_{segment['color']}_{i}"
        plot_lines_tags[stock["ISIN"]].append(tag)
        dpg.add_line_series(
            [point[0] for point in segment["points"]],
            [point[1] for point in segment["points"]],
            parent=f"{stock['ISIN']}_y_axis",
            tag=tag,
        )
        apply_line_color_to(cfg, tag, segment["color"])
        i += 1

    dpg.fit_axis_data(f"{stock['ISIN']}_x_axis")
    dpg.fit_axis_data(f"{stock['ISIN']}_y_axis")


def change_period(sender, period: str, user_data: dict):
    cfg = user_data["cfg"]
    stock = user_data["stock"]
    ticker = yfinance.Ticker(stock["ISIN"])
    history = ticker.history(
        period=cfg["ui"]["periods"][period],
        repair=True,
        prepost=True,
    )
    price_history[stock["ISIN"]] = history["Close"].tolist()
    date_history[stock["ISIN"]] = [
        int(date.timestamp()) for date in history.index.tolist()
    ]
    update_graph(cfg, stock)


def render_plots(cfg: dict):
    delete_plots(cfg)

    position_x = 0
    position_y = 21

    with dpg.window(tag="plots"):
        for stock in cfg["stocks"]:
            with dpg.window(
                label=f"{stock['name']}",
                tag=f"plot_{stock['ISIN']}",
                width=cfg["ui"]["graph_initial_width"],
                height=cfg["ui"]["graph_initial_height"],
                pos=(position_x, position_y),
            ):
                with dpg.plot(
                    crosshairs=True,
                    no_title=True,
                ):
                    dpg.add_plot_axis(
                        dpg.mvXAxis,
                        tag=f"{stock['ISIN']}_x_axis",
                        time=True,
                        no_tick_labels=False,
                        no_gridlines=True,
                    )
                    dpg.add_plot_axis(
                        dpg.mvYAxis,
                        tag=f"{stock['ISIN']}_y_axis",
                        user_data={"stock": stock},
                    )
                    dpg.add_line_series(
                        [],
                        [],
                        tag=f"Plot_{stock['ISIN']}",
                        parent=f"{stock['ISIN']}_y_axis",
                    )
                dpg.add_combo(
                    default_value=cfg["ui"]["default_time_range"],
                    items=list(cfg["ui"]["periods"].keys()),
                    callback=change_period,
                    user_data={"cfg": cfg, "stock": stock},
                    width=100,
                )
            if (
                position_y
                + 3
                + cfg["ui"]["graph_initial_height"]
                + cfg["ui"]["graph_initial_height"]
                > cfg["ui"]["screen_height"]
            ):
                position_x += cfg["ui"]["graph_initial_width"] + 3
                position_y = 21
            else:
                position_y += cfg["ui"]["graph_initial_height"] + 3

    dpg.set_primary_window("plots", True)


def delete_plots(cfg: dict):
    if dpg.does_item_exist("plots"):
        dpg.delete_item("plots")
