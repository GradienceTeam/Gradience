# preset.py
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
import os

from ..settings_schema import settings_schema
from .utils import buglog, to_slug_case
from .css import load_preset_from_css
import random
presets_dir = os.path.join(
    os.environ.get("XDG_CONFIG_HOME", os.environ["HOME"] + "/.config"),
    "presets",
)

AMAZING_NAMES = [
    "Amazing",
    "Wonderful",
    "My Preset",
    "Splendide",
    "Magnifique",
    "Cool",
    "Superbe",
    "Awesome"
]


class ItWasAPreset:
    variables = {}
    palette = {}
    custom_css = {
        "gtk4": "",
        "gtk3": "",
    }
    plugins = {}
    repo = "user"
    name = "new_preset"
    badges = {}

    def __init__(self, name=None, repo=None, preset_path=None, text=None, preset=None):
        if text:  # load from ressource
            self.load_preset(text=text)
        elif preset:  # css or dict
            self.load_preset(preset=preset)
        else:
            self.preset_name = name
            if name is not None:
                self.name = to_slug_case(name)
            if repo is not None:
                self.repo = repo
            if preset_path is None:
                self.preset_path = os.path.join(
                    presets_dir, repo, self.name + ".json")
            else:
                self.preset_path = preset_path
            self.load_preset()

    def load_preset(self, text=None, preset=None):
        try:
            if not preset:
                if text:
                    preset_text = text
                else:
                    with open(self.preset_path, "r", encoding="utf-8") as file:
                        preset_text = file.read()
                preset = json.loads(preset_text)

            self.name = preset["name"]
            self.preset_name = to_slug_case(self.name)
            self.variables = preset["variables"]
            self.palette = preset["palette"]

            if "badges" in preset:
                self.badges = preset["badges"]
            else:
                self.badges = {}

            if "custom_css" in preset:
                self.custom_css = preset["custom_css"]
            else:
                for app_type in settings_schema["custom_css_app_types"]:
                    self.custom_css[app_type] = ""
        except Exception as error:
            buglog(error, " -> preset : ", self.preset_path)

    def save_preset(self, name=None, plugins_list=None, to=None):
        if to is None:
            self.preset_path = os.path.join(
                presets_dir, self.repo, self.name + ".json")
        else:
            self.preset_path = to
        if not os.path.exists(
            os.path.join(
                presets_dir,
                "user",
            )
        ):
            os.makedirs(
                os.path.join(
                    presets_dir,
                    "user",
                )
            )

        if name is None:
            name = self.preset_name

        if plugins_list is None:
            plugins_list = {}
        else:
            plugins_list = plugins_list.save()

        with open(
            self.preset_path,
            "w",
            encoding="utf-8",
        ) as file:
            object_to_write = {
                "name": name,
                "variables": self.variables,
                "palette": self.palette,
                "custom_css": self.custom_css,
                "plugins": plugins_list,
            }
            file.write(json.dumps(object_to_write, indent=4))

    def validate(self):
        return True

class DarkPreset(BasePreset):
    def no_preset(self):

        self.variables = {
            "accent_color": "#78aeed",
            "accent_bg_color": "#3584e4",
            "accent_fg_color": "#ffffff",
            "destructive_color": "#ff7b63",
            "destructive_bg_color": "#c01c28",
            "destructive_fg_color": "#ffffff",
            "success_color": "#8ff0a4",
            "success_bg_color": "#26a269",
            "success_fg_color": "#ffffff",
            "warning_color": "#f8e45c",
            "warning_bg_color": "#cd9309",
            "warning_fg_color": "rgba(0, 0, 0, 0.8)",
            "error_color": "#ff7b63",
            "error_bg_color": "#c01c28",
            "error_fg_color": "#ffffff",
            "window_bg_color": "#242424",
            "window_fg_color": "#ffffff",
            "view_bg_color": "#1e1e1e",
            "view_fg_color": "#ffffff",
            "headerbar_bg_color": "#303030",
            "headerbar_fg_color": "#ffffff",
            "headerbar_border_color": "#ffffff",
            "headerbar_backdrop_color": "@window_bg_color",
            "headerbar_shade_color": "rgba(0, 0, 0, 0.36)",
            "card_bg_color": "rgba(255, 255, 255, 0.08)",
            "card_fg_color": "#ffffff",
            "card_shade_color": "rgba(0, 0, 0, 0.36)",
            "dialog_bg_color": "#383838",
            "dialog_fg_color": "#ffffff",
            "popover_bg_color": "#383838",
            "popover_fg_color": "#ffffff",
            "shade_color": "rgba(0,0,0,0.36)",
            "scrollbar_outline_color": "rgba(0,0,0,0.5)"
        }
        self.palette = {
            "blue_": {
                "1": "#99c1f1",
                "2": "#62a0ea",
                "3": "#3584e4",
                "4": "#1c71d8",
                "5": "#1a5fb4"
            },
            "green_": {
                "1": "#8ff0a4",
                "2": "#57e389",
                "3": "#33d17a",
                "4": "#2ec27e",
                "5": "#26a269"
            },
            "yellow_": {
                "1": "#f9f06b",
                "2": "#f8e45c",
                "3": "#f6d32d",
                "4": "#f5c211",
                "5": "#e5a50a"
            },
            "orange_": {
                "1": "#ffbe6f",
                "2": "#ffa348",
                "3": "#ff7800",
                "4": "#e66100",
                "5": "#c64600"
            },
            "red_": {
                "1": "#f66151",
                "2": "#ed333b",
                "3": "#e01b24",
                "4": "#c01c28",
                "5": "#a51d2d"
            },
            "purple_": {
                "1": "#dc8add",
                "2": "#c061cb",
                "3": "#9141ac",
                "4": "#813d9c",
                "5": "#613583"
            },
            "brown_": {
                "1": "#cdab8f",
                "2": "#b5835a",
                "3": "#986a44",
                "4": "#865e3c",
                "5": "#63452c"
            },
            "light_": {
                "1": "#ffffff",
                "2": "#f6f5f4",
                "3": "#deddda",
                "4": "#c0bfbc",
                "5": "#9a9996"
            },
            "dark_": {
                "1": "#77767b",
                "2": "#5e5c64",
                "3": "#3d3846",
                "4": "#241f31",
                "5": "#000000"
            }
        }


class LightPreset(BasePreset):

    def no_preset(self):
        self.variables = {
            "accent_color": "#1c71d8",
            "accent_bg_color": "#3584e4",
            "accent_fg_color": "#ffffff",
            "destructive_color": "#c01c28",
            "destructive_bg_color": "#e01b24",
            "destructive_fg_color": "#ffffff",
            "success_color": "#26a269",
            "success_bg_color": "#2ec27e",
            "success_fg_color": "#ffffff",
            "warning_color": "#ae7b03",
            "warning_bg_color": "#e5a50a",
            "warning_fg_color": "rgba(0, 0, 0, 0.8)",
            "error_color": "#c01c28",
            "error_bg_color": "#e01b24",
            "error_fg_color": "#ffffff",
            "window_bg_color": "#fafafa",
            "window_fg_color": "rgba(0, 0, 0, 0.8)",
            "view_bg_color": "#ffffff",
            "view_fg_color": "#000000",
            "headerbar_bg_color": "#ebebeb",
            "headerbar_fg_color": "rgba(0, 0, 0, 0.8)",
            "headerbar_border_color": "rgba(0, 0, 0, 0.8)",
            "headerbar_backdrop_color": "@window_bg_color",
            "headerbar_shade_color": "rgba(0, 0, 0, 0.07)",
            "card_bg_color": "#ffffff",
            "card_fg_color": "rgba(0, 0, 0, 0.8)",
            "card_shade_color": "rgba(0, 0, 0, 0.07)",
            "dialog_bg_color": "#fafafa",
            "dialog_fg_color": "rgba(0, 0, 0, 0.8)",
            "popover_bg_color": "#ffffff",
            "popover_fg_color": "rgba(0, 0, 0, 0.8)",
            "shade_color": "rgba(0,0,0,0.07)",
            "scrollbar_outline_color": "rgb(255,255,255)"
        }
        self.palette = {
            "blue_": {
                "1": "#99c1f1",
                "2": "#62a0ea",
                "3": "#3584e4",
                "4": "#1c71d8",
                "5": "#1a5fb4"
            },
            "green_": {
                "1": "#8ff0a4",
                "2": "#57e389",
                "3": "#33d17a",
                "4": "#2ec27e",
                "5": "#26a269"
            },
            "yellow_": {
                "1": "#f9f06b",
                "2": "#f8e45c",
                "3": "#f6d32d",
                "4": "#f5c211",
                "5": "#e5a50a"
            },
            "orange_": {
                "1": "#ffbe6f",
                "2": "#ffa348",
                "3": "#ff7800",
                "4": "#e66100",
                "5": "#c64600"
            },
            "red_": {
                "1": "#f66151",
                "2": "#ed333b",
                "3": "#e01b24",
                "4": "#c01c28",
                "5": "#a51d2d"
            },
            "purple_": {
                "1": "#dc8add",
                "2": "#c061cb",
                "3": "#9141ac",
                "4": "#813d9c",
                "5": "#613583"
            },
            "brown_": {
                "1": "#cdab8f",
                "2": "#b5835a",
                "3": "#986a44",
                "4": "#865e3c",
                "5": "#63452c"
            },
            "light_": {
                "1": "#ffffff",
                "2": "#f6f5f4",
                "3": "#deddda",
                "4": "#c0bfbc",
                "5": "#9a9996"
            },
            "dark_": {
                "1": "#77767b",
                "2": "#5e5c64",
                "3": "#3d3846",
                "4": "#241f31",
                "5": "#000000"
            }
        }


class Preset():
    description = ""
    plugins = {}
    badges = {}
    repo = ""
    filename = ""
    name = ""
    default = "light"

    def __init__(self, name=None, repo="user", dark=None, dark_path=None, dark_css=None, light=None, light_path=None, light_css=None, default="light"):
        if dark:
            self.dark = DarkPreset(preset=dark)
        elif dark_path:
            self.dark = DarkPreset(preset_path=dark_path)
        elif dark_css:
            self.dark = DarkPreset(css=dark_css)
        else:
            self.dark = DarkPreset()

        if light:
            self.light = LightPreset(preset=light)
        elif light_path:
            self.light = LightPreset(preset_path=light_path)
        elif light_css:
            self.light = LightPreset(css=light_css)
        else:
            self.light = LightPreset()

        if name is not None:
            self.name = name
        else:
            self.name = random.choice(AMAZING_NAMES)
        self.filename = to_slug_case(self.name)
        self.repo = repo
        self.default = default

    def load_dark(self, css=None, preset=None, preset_path=None):
        self.dark = DarkPreset(css, preset, preset_path)

    def load_light(self, css=None, preset=None, preset_path=None):
        self.light = LightPreset(css, preset, preset_path)

    def load_from_file(self, path):
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file.read())

        # user/preset.json
        # -2    -1
        self.repo = path.split("/")[-2]
        self.name = data["name"] if "name" in data else random.choice(AMAZING_NAMES)
        self.filename = to_slug_case(self.name)
        self.description = data["description"] if "description" in data else ""
        self.badges = data["badges"] if "badges" in data else {}
        self.default = data["default"] if "default" in data else "light"
        self.dark = DarkPreset(preset=data["dark"]) if "dark" in data else DarkPreset()
        self.light = LightPreset(preset=data["light"]) if "light" in data else LightPreset()

    def __repr__(self):
        return f"Preset({self.name})"

    @property
    def variables(self):
        return self.light.variables if self.default == "light" else self.dark.variables

    @property
    def pallette(self):
        return self.light.palette if self.default == "light" else self.dark.palette

    def to_json(self):
        return {
            "name": self.name,
            "description": self.description,
            "plugins": self.plugins,
            "badges": self.badges,
            "dark": self.dark.to_json(),
            "light": self.light.to_json(),
            "default": self.default
        }

    def save(self, to=None):
        if to is None:
            to = os.path.join(presets_dir, self.repo, self.filename + ".json")
        with open(to, "w", encoding="utf-8") as file:
            file.write(json.dumps(self.to_json(), indent=4))

if __name__ == "__main__":
    p = Preset()
    buglog(p.variables)
    buglog(p.palette)
