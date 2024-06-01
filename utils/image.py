import dearpygui.dearpygui as dpg

images = {}

def insert_image(
    image_path: str,
    parent=None,
    width: int = None,
    height: int = None,
    size_percent: int = None,
    tag=0,
):

    if image_path not in images:
        original_width, original_height, channels, data = dpg.load_image(image_path)

        with dpg.texture_registry() as reg_id:
            texture_id = dpg.add_static_texture(
                width=original_width,
                height=original_height,
                default_value=data,
                parent=reg_id,
            )
        images[image_path] = {
            "original_width": original_width,
            "original_height": original_height,
            "texture_id": texture_id,
        }
    else:
        original_width = images[image_path]["original_width"]
        original_height = images[image_path]["original_height"]
        texture_id = images[image_path]["texture_id"]

    if width is None:
        width = original_width
    if height is None:
        height = original_height
    if size_percent is not None:
        size_percent = size_percent / 100
        width = width * size_percent
        height = height * size_percent

    if parent is None:
        return dpg.add_image(texture_id, width=width, height=height, tag=tag)
    else:
        return dpg.add_image(
            texture_id, width=width, height=height, parent=parent, tag=tag
        )
