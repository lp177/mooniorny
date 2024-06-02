import uuid
import dearpygui.dearpygui as dpg


def modal(
    text: str = None,
    label: str = None,
    tag=0,
    width: int = 300,
    height: int = 200,
    show: bool = True,
    modal: bool = True,
    padding_size: int = 30,
    color: tuple = (250, 250, 250),
):
    top = int(dpg.get_viewport_height() / 2 - (height / 2))
    left = int(dpg.get_viewport_width() / 2 - (width / 2))
    if left < 0:
        left = 0
    if top < 0:
        top = 0
    if tag == 0:
        tag = uuid.uuid4()
    with dpg.window(
        label=label,
        tag=tag,
        width=width,
        height=height,
        pos=(left, top),
        show=show,
        modal=modal,
        on_close=lambda: dpg.delete_item(tag),
    ) as window:
        if text is not None:
            dpg.add_text(text, color=color)
    with dpg.theme() as padding:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_style(
                dpg.mvStyleVar_WindowPadding,
                padding_size,
                padding_size,
                category=dpg.mvThemeCat_Core,
            )
    dpg.bind_item_theme(window, padding)
