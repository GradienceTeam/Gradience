# monet.py
#
# Change the look of Adwaita, with ease
# Copyright (C) 2022 Gradience Team
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

import os

import material_color_utilities_python as monet

from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM

from gradience.backend.models.preset import Preset
from gradience.backend.utils.colors import argb_to_color_code

from gradience.backend.logger import Logger

logging = Logger()


class Monet:
    def __init__(self):
        self.palette = None

    def generate_palette_from_image(self, image_path: str) -> dict:
        if image_path.endswith(".svg"):
            drawing = svg2rlg(image_path)
            image_path = os.path.join(
                os.environ.get("XDG_RUNTIME_DIR"), "gradience_bg.png"
            )
            renderPM.drawToFile(drawing, image_path, fmt="PNG")

        if image_path.endswith(".xml"):
            # TODO: Use custom exception in future
            raise ValueError("XML files are unsupported by Gradience's Monet implementation")

        try:
            monet_img = monet.Image.open(image_path)
        except Exception as e:
            logging.error("An error occurred while generating a Monet palette.", exc=e)
            raise
        else:
            basewidth = 64
            wpercent = basewidth / float(monet_img.size[0])
            hsize = int((float(monet_img.size[1]) * float(wpercent)))

            monet_img = monet_img.resize(
                (basewidth, hsize), monet.Image.Resampling.LANCZOS
            )

            self.palette = monet.themeFromImage(monet_img)

        return self.palette

    def new_preset_from_monet(self, name=None, monet_palette=None, props=None, obj_only=False) -> Preset or None:
        preset = Preset()

        if props:
            tone = props[0]
            theme = props[1]
        else:
            raise AttributeError("Properties 'tone' and/or 'theme' missing")

        if not monet_palette:
            raise AttributeError("Property 'monet_palette' missing")

        if theme == "light":
            light_theme = monet_palette["schemes"]["light"]
            variable = {
                "accent_color": argb_to_color_code(light_theme.primary),
                "accent_bg_color": argb_to_color_code(light_theme.primary),
                "accent_fg_color": argb_to_color_code(light_theme.onPrimary),
                "destructive_color": argb_to_color_code(light_theme.error),
                "destructive_bg_color": argb_to_color_code(light_theme.errorContainer),
                # Avoid using .onError as it causes contrast issues
                "destructive_fg_color": argb_to_color_code(light_theme.onErrorContainer),
                "success_color": argb_to_color_code(light_theme.tertiary),
                "success_bg_color": argb_to_color_code(light_theme.tertiaryContainer),
                "success_fg_color": argb_to_color_code(light_theme.onTertiaryContainer),
                "warning_color": argb_to_color_code(light_theme.secondary),
                "warning_bg_color": argb_to_color_code(light_theme.secondaryContainer),
                "warning_fg_color": argb_to_color_code(light_theme.onSecondaryContainer),
                "error_color": argb_to_color_code(light_theme.error),
                "error_bg_color": argb_to_color_code(light_theme.errorContainer),
                # Avoid using .onError as it causes contrast issues
                "error_fg_color": argb_to_color_code(light_theme.onErrorContainer),
                "window_bg_color": argb_to_color_code(light_theme.surface),
                "window_fg_color": argb_to_color_code(light_theme.onSurface),
                "view_bg_color": argb_to_color_code(light_theme.secondaryContainer),
                "view_fg_color": argb_to_color_code(light_theme.onSurface),
                "headerbar_bg_color": argb_to_color_code(light_theme.secondaryContainer),
                "headerbar_fg_color": argb_to_color_code(light_theme.onSecondaryContainer),
                "headerbar_border_color": argb_to_color_code(light_theme.onSurface, "0.8"),
                "headerbar_backdrop_color": "@window_bg_color",
                "headerbar_shade_color": argb_to_color_code(light_theme.onSurface, "0.07"),
                "card_bg_color": argb_to_color_code(light_theme.primary, "0.05"),
                "card_fg_color": argb_to_color_code(light_theme.onSecondaryContainer),
                "card_shade_color": argb_to_color_code(light_theme.shadow, "0.07"),
                "thumbnail_bg_color": argb_to_color_code(light_theme.secondaryContainer),
                "thumbnail_fg_color": argb_to_color_code(light_theme.onSecondaryContainer),
                "dialog_bg_color": argb_to_color_code(light_theme.secondaryContainer),
                "dialog_fg_color": argb_to_color_code(light_theme.onSecondaryContainer),
                "popover_bg_color": argb_to_color_code(light_theme.secondaryContainer),
                "popover_fg_color": argb_to_color_code(light_theme.onSecondaryContainer),
                "shade_color": argb_to_color_code(light_theme.shadow, "0.07"),
                "scrollbar_outline_color": argb_to_color_code(light_theme.outline),
            }
        elif theme == "dark":
            dark_theme = monet_palette["schemes"]["dark"]
            variable = {
                "accent_color": argb_to_color_code(dark_theme.primary),
                "accent_bg_color": argb_to_color_code(dark_theme.primary),
                "accent_fg_color": argb_to_color_code(dark_theme.onPrimary),
                "destructive_color": argb_to_color_code(dark_theme.error),
                "destructive_bg_color": argb_to_color_code(dark_theme.errorContainer),
                # Avoid using .onError as it causes contrast issues
                "destructive_fg_color": argb_to_color_code(dark_theme.onErrorContainer),
                "success_color": argb_to_color_code(dark_theme.tertiary),
                "success_bg_color": argb_to_color_code(dark_theme.tertiaryContainer),
                "success_fg_color": argb_to_color_code(dark_theme.onTertiaryContainer),
                "warning_color": argb_to_color_code(dark_theme.secondary),
                "warning_bg_color": argb_to_color_code(dark_theme.secondaryContainer),
                "warning_fg_color": argb_to_color_code(dark_theme.onSecondaryContainer),
                "error_color": argb_to_color_code(dark_theme.error),
                "error_bg_color": argb_to_color_code(dark_theme.errorContainer),
                # Avoid using .onError as it causes contrast issues
                "error_fg_color": argb_to_color_code(dark_theme.onErrorContainer),
                "window_bg_color": argb_to_color_code(dark_theme.surface),
                "window_fg_color": argb_to_color_code(dark_theme.onSurface),
                "view_bg_color": argb_to_color_code(dark_theme.secondaryContainer),
                "view_fg_color": argb_to_color_code(dark_theme.onSurface),
                "headerbar_bg_color": argb_to_color_code(dark_theme.secondaryContainer),
                "headerbar_fg_color": argb_to_color_code(dark_theme.onSecondaryContainer),
                "headerbar_border_color": argb_to_color_code(dark_theme.onSurface, "0.8"),
                "headerbar_backdrop_color": "@window_bg_color",
                "headerbar_shade_color": argb_to_color_code(dark_theme.onSurface, "0.07"),
                "card_bg_color": argb_to_color_code(dark_theme.primary, "0.05"),
                "card_fg_color": argb_to_color_code(dark_theme.onSecondaryContainer),
                "card_shade_color": argb_to_color_code(dark_theme.shadow, "0.07"),
                "thumbnail_bg_color": argb_to_color_code(dark_theme.secondaryContainer),
                "thumbnail_fg_color": argb_to_color_code(dark_theme.onSecondaryContainer),
                "dialog_bg_color": argb_to_color_code(dark_theme.secondaryContainer),
                "dialog_fg_color": argb_to_color_code(dark_theme.onSecondaryContainer),
                "popover_bg_color": argb_to_color_code(dark_theme.secondaryContainer),
                "popover_fg_color": argb_to_color_code(dark_theme.onSecondaryContainer),
                "shade_color": argb_to_color_code(dark_theme.shadow, "0.36"),
                "scrollbar_outline_color": argb_to_color_code(dark_theme.outline, "0.5"),
            }
        else:
            raise AttributeError("Unknown theme variant selected")

        if obj_only == False and not name:
            raise AttributeError("You either need to set 'obj_only' property to True, or add value to 'name' property")

        if obj_only:
            if name:
                preset.new(variables=variable, display_name=name)
            else:
                preset.new(variables=variable)
            return preset

        if obj_only == False:
            preset.new(variables=variable, display_name=name)

            try:
                preset.save_to_file()
            except OSError:
                raise
