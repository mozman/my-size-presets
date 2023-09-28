# Copyright (C) 2023, Manfred Moitzi
# License: MIT License
from __future__ import annotations

import gradio as gr
from modules import scripts
from modules.ui_components import FormRow

TITLE = "My Personal Image Size Presets"
MIN_WIDTH = 120
HEADER =  [
    "Presets",
    "Portrait",
    "Portrait",
    "Square",
    "Landscape",
    "Landscape",
    "Widescreen",
]

SD15_512_PRESETS = "SD15 - 512px", [
    "512x768 (2:3)",
    "512x672 (3:4)",
    "512x512 (1:1)",
    "672x512 (4:3)",
    "768x512 (3:2)",
    "896x512 (16:9)",
]
SD15_640_PRESETS = "SD15 - 640px", [
    "640x960 (2:3)",
    "640x848 (3:4)",
    "640x640 (1:1)",
    "848x640 (4:3)",
    "960x640 (3:2)",
    "1136x640 (16:9)",
]
SDXL_PRESETS = "SDXL", [
    "832x1216 (2:3)",
    "896x1152 (3:4)",
    "1024x1024 (1:1)",
    "1152x896 (4:3)",
    "1216x832 (3:2)",
    "1344x768 (16:9)",
]

PRESETS = [
    SD15_512_PRESETS, SD15_640_PRESETS, SDXL_PRESETS
]
DEFAULT_WIDTH_HEIGHT = 512, 512


class MySizePresets(scripts.Script):
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
        if is_img2img:
            wc, hc = self.i2i_w, self.i2i_h
        else:
            wc, hc = self.t2i_w, self.t2i_h

        outputs = [wc, hc]
        with gr.Group():
            with gr.Accordion("My Size Presets", open=False):
                with FormRow():
                    for value in HEADER:
                        gr.Button(value=value, interactive=False, min_width=MIN_WIDTH)
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
