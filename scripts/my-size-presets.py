# Copyright (C) 2023, Manfred Moitzi
# License: MIT License
from __future__ import annotations

import gradio as gr
from modules import scripts
from modules.ui_components import FormRow

TITLE = "My Image Size Presets"
MIN_WIDTH = 120

# All values are multiples of 64!
PRESET_512 = "512", [
    "512x512 (1:1)",
    "704x512 (4:3)",  # 1.375 > 1.333 (4.1:3)
    "768x512 (3:2)",  # 1.500 = 1.500
    "896x512 (16:9)",  # 1.750 < 1.777 (15.8:9)
]
PRESET_640 = "640", [
    "640x640 (1:1)",
    "832x640 (4:3)",  # 1.300 < 1.333 (3.9:3)
    "960x640 (3:2)",  # 1.500 = 1.500
    "1152x640 (16:9)",  # 1.800 > 1.777 (16.2:9)
]
PRESET_768 = "768", [
    "768x768 (1:1)",
    "1024x768 (4:3)",  # 1.333 = 1.333
    "1152x768 (3:2)",  # 1.500 = 1.500
    "1344x768 (16:9)",  # 1.750 < 1.777 (15.8:9)
]
PRESET_SDXL = "SDXL", [
    "1024x1024 (1:1)",
    "1152x896 (4:3)",  # 1.286 < 1.333 (3.9:3)
    "1280x832 (3:2)",  # 1.539 > 1.500 (3.1:4)
    # 1344x768 (16:9) => PRESET_768
    "1536x640 (21:9)",  # 2.400 < 2.333 (21.6:9)
]

PRESETS = [PRESET_512, PRESET_640, PRESET_768, PRESET_SDXL]
DEFAULT_WIDTH_HEIGHT = 512, 512


class MyImageSizePresets(scripts.Script):
    def __init__(self):
        self.t2i_w: gr.components.Slider | None = None
        self.t2i_h: gr.components.Slider | None = None
        self.i2i_w: gr.components.Slider | None = None
        self.i2i_h: gr.components.Slider | None = None

    def title(self) -> str:
        return TITLE

    def show(self, is_img2img: bool):
        return scripts.AlwaysVisible

    def ui(self, is_img2img: bool):
        outputs = [self.i2i_w, self.i2i_h] if is_img2img else [self.t2i_w, self.t2i_h]
        with gr.Group():
            with gr.Accordion(TITLE, open=False):
                for label, presets in PRESETS:
                    with FormRow():
                        gr.Button(value=label, min_width=MIN_WIDTH, interactive=False)
                        for value in presets:
                            button = gr.Button(value=value, min_width=MIN_WIDTH)
                            button.click(
                                fn=get_dimensions, inputs=[button], outputs=outputs
                            )
        return []

    def after_component(self, component: gr.components.Component, **kwargs):
        element_id = kwargs.get("elem_id")
        if isinstance(component, gr.components.Slider):
            if element_id == "txt2img_width":
                self.t2i_w: gr.components.Slider = component
            elif element_id == "txt2img_height":
                self.t2i_h: gr.components.Slider = component
            elif element_id == "img2img_width":
                self.i2i_w: gr.components.Slider = component
            elif element_id == "img2img_height":
                self.i2i_h: gr.components.Slider = component


def get_dimensions(value: str) -> tuple[int, int]:
    # format: 512x512 any text
    try:
        wh, _ = value.split(" ")
        width, height = wh.split("x")
        return int(width), int(height)
    except ValueError:
        return DEFAULT_WIDTH_HEIGHT
