# preset_utils.py
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

import json
import material_color_utilities_python as monet

from gradience.backend.theming.monet import Monet
from gradience.backend.models.preset import Preset
from gradience.backend.utils.colors import rgba_from_argb

from gradience.backend.logger import Logger

logging = Logger()


class PresetUtils:
    def __init__(self):
        self.preset = Preset()

    def new_preset_from_monet(self, name=None, monet_palette=None, props=None, vars_only=False) -> dict or bool:
        if props:
            tone = props[0]
            theme = props[1]
        else:
            raise Exception("Properties 'tone' and/or 'theme' missing")

        if not monet_palette:
            raise Exception("Property 'monet_palette' missing")

        if theme == "dark":
            dark_theme = monet_palette["schemes"]["dark"]
            variable = {
                "accent_color": rgba_from_argb(dark_theme.primary),
                "accent_bg_color": rgba_from_argb(dark_theme.primaryContainer),
                "accent_fg_color": rgba_from_argb(dark_theme.onPrimaryContainer),
                "destructive_color": rgba_from_argb(dark_theme.error),
                "destructive_bg_color": rgba_from_argb(dark_theme.errorContainer),
                "destructive_fg_color": rgba_from_argb(
                    dark_theme.onErrorContainer
                ),
                "success_color": rgba_from_argb(dark_theme.tertiary),
                "success_bg_color": rgba_from_argb(dark_theme.onTertiary),
                "success_fg_color": rgba_from_argb(dark_theme.onTertiaryContainer),
                "warning_color": rgba_from_argb(dark_theme.secondary),
                "warning_bg_color": rgba_from_argb(dark_theme.onSecondary),
                "warning_fg_color": rgba_from_argb(dark_theme.primary, "0.8"),
                "error_color": rgba_from_argb(dark_theme.error),
                "error_bg_color": rgba_from_argb(dark_theme.errorContainer),
                "error_fg_color": rgba_from_argb(dark_theme.onError),
                "window_bg_color": rgba_from_argb(dark_theme.surface),
                "window_fg_color": rgba_from_argb(dark_theme.onSurface),
                "view_bg_color": rgba_from_argb(dark_theme.surface),
                "view_fg_color": rgba_from_argb(dark_theme.onSurface),
                "headerbar_bg_color": rgba_from_argb(dark_theme.surface),
                "headerbar_fg_color": rgba_from_argb(dark_theme.onSurface),
                "headerbar_border_color": rgba_from_argb(
                    dark_theme.primary, "0.8"
                ),
                "headerbar_backdrop_color": "@headerbar_bg_color",
                "headerbar_shade_color": rgba_from_argb(dark_theme.shadow),
                "card_bg_color": rgba_from_argb(dark_theme.primary, "0.05"),
                "card_fg_color": rgba_from_argb(dark_theme.onSecondaryContainer),
                "card_shade_color": rgba_from_argb(dark_theme.shadow),
                "dialog_bg_color": rgba_from_argb(dark_theme.secondaryContainer),
                "dialog_fg_color": rgba_from_argb(dark_theme.onSecondaryContainer),
                "popover_bg_color": rgba_from_argb(dark_theme.secondaryContainer),
                "popover_fg_color": rgba_from_argb(
                    dark_theme.onSecondaryContainer
                ),
                "shade_color": rgba_from_argb(dark_theme.shadow),
                "scrollbar_outline_color": rgba_from_argb(dark_theme.outline),
            }
        elif theme == "light":
            light_theme = monet_palette["schemes"]["light"]
            variable = {
                "accent_color": rgba_from_argb(light_theme.primary),
                "accent_bg_color": rgba_from_argb(light_theme.primary),
                "accent_fg_color": rgba_from_argb(light_theme.onPrimary),
                "destructive_color": rgba_from_argb(light_theme.error),
                "destructive_bg_color": rgba_from_argb(light_theme.errorContainer),
                "destructive_fg_color": rgba_from_argb(
                    light_theme.onErrorContainer
                ),
                "success_color": rgba_from_argb(light_theme.tertiary),
                "success_bg_color": rgba_from_argb(light_theme.tertiaryContainer),
                "success_fg_color": rgba_from_argb(
                    light_theme.onTertiaryContainer
                ),
                "warning_color": rgba_from_argb(light_theme.secondary),
                "warning_bg_color": rgba_from_argb(light_theme.secondaryContainer),
                "warning_fg_color": rgba_from_argb(
                    light_theme.onSecondaryContainer
                ),
                "error_color": rgba_from_argb(light_theme.error),
                "error_bg_color": rgba_from_argb(light_theme.errorContainer),
                "error_fg_color": rgba_from_argb(light_theme.onError),
                "window_bg_color": rgba_from_argb(light_theme.secondaryContainer),
                "window_fg_color": rgba_from_argb(light_theme.onSurface),
                "view_bg_color": rgba_from_argb(light_theme.secondaryContainer),
                "view_fg_color": rgba_from_argb(light_theme.onSurface),
                "headerbar_bg_color": rgba_from_argb(
                    light_theme.secondaryContainer
                ),
                "headerbar_fg_color": rgba_from_argb(light_theme.onSurface),
                "headerbar_border_color": rgba_from_argb(
                    light_theme.primary, "0.8"
                ),
                "headerbar_backdrop_color": "@headerbar_bg_color",
                "headerbar_shade_color": rgba_from_argb(
                    light_theme.secondaryContainer
                ),
                "card_bg_color": rgba_from_argb(light_theme.primary, "0.05"),
                "card_fg_color": rgba_from_argb(light_theme.onSecondaryContainer),
                "card_shade_color": rgba_from_argb(light_theme.shadow),
                "dialog_bg_color": rgba_from_argb(light_theme.secondaryContainer),
                "dialog_fg_color": rgba_from_argb(
                    light_theme.onSecondaryContainer
                ),
                "popover_bg_color": rgba_from_argb(light_theme.secondaryContainer),
                "popover_fg_color": rgba_from_argb(
                    light_theme.onSecondaryContainer
                ),
                "shade_color": rgba_from_argb(light_theme.shadow),
                "scrollbar_outline_color": rgba_from_argb(light_theme.outline),
            }

        if vars_only == False and not name:
            raise Exception("You either need to set 'vars_only' property to True, or add value to 'name' property")

        if vars_only:
            return variable

        self.preset.new(display_name=name, variables=variable)

        '''preset_dict = {
            "name": self.preset.display_name,
            "variables": self.preset.variables,
            "palette": self.preset.palette,
            "custom_css": self.preset.custom_css,
            "plugins": self.preset.plugins,
        }
        logging.debug("Generated Monet preset:\n" + json.dumps(preset_dict, indent=4))'''

        try:
            self.preset.save_to_file(name=name)
        except Exception as e:
            # TODO: Move exception handling to model/preset module
            logging.error(f"Unexpected file error while trying to generate preset from generated Monet palette. Exc: {e}")
            return False

        return True

if __name__ == "__main__":
    preset_utils = PresetUtils()

    monet_palette = Monet().generate_from_image("/home/tfuxc/Pictures/Wallpapers/wallhaven-57kzw1.png")
    props = [20, "dark"]

    preset_utils.new_preset_from_monet("My awesome Monet", monet_palette, props)
