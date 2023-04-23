# preset.py
#
# Change the look of Adwaita, with ease
# Copyright (C) 2022-2023, Gradience Team
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

from gradience.backend.utils.common import to_slug_case
from gradience.backend.globals import presets_dir

from gradience.backend.logger import Logger

logging = Logger()


# Adwaita default colors palette dict
adw_palette = {
    "blue_": {
        "1": "#99c1f1",
        "2": "#62a0ea",
        "3": "#3584e4",
        "4": "#1c71d8",
        "5": "#1a5fb4",
    },
    "green_": {
        "1": "#8ff0a4",
        "2": "#57e389",
        "3": "#33d17a",
        "4": "#2ec27e",
        "5": "#26a269",
    },
    "yellow_": {
        "1": "#f9f06b",
        "2": "#f8e45c",
        "3": "#f6d32d",
        "4": "#f5c211",
        "5": "#e5a50a",
    },
    "orange_": {
        "1": "#ffbe6f",
        "2": "#ffa348",
        "3": "#ff7800",
        "4": "#e66100",
        "5": "#c64600",
    },
    "red_": {
        "1": "#f66151",
        "2": "#ed333b",
        "3": "#e01b24",
        "4": "#c01c28",
        "5": "#a51d2d",
    },
    "purple_": {
        "1": "#dc8add",
        "2": "#c061cb",
        "3": "#9141ac",
        "4": "#813d9c",
        "5": "#613583",
    },
    "brown_": {
        "1": "#cdab8f",
        "2": "#b5835a",
        "3": "#986a44",
        "4": "#865e3c",
        "5": "#63452c",
    },
    "light_": {
        "1": "#ffffff",
        "2": "#f6f5f4",
        "3": "#deddda",
        "4": "#c0bfbc",
        "5": "#9a9996",
    },
    "dark_": {
        "1": "#77767b",
        "2": "#5e5c64",
        "3": "#3d3846",
        "4": "#241f31",
        "5": "#000000",
    }
}

# Supported GTK versions that can utilize custom CSS
custom_css_gtk_versions = [
    "gtk4",
    "gtk3"
]


class Preset:
    display_name = "New Preset"
    preset_path = "new_preset"

    variables = {}
    palette = adw_palette
    custom_css = {
        "gtk4": "",
        "gtk3": ""
    }

    plugins = {}
    plugins_list = {}
    badges = {}

    def __init__(self):
        pass

    def new(self, variables: dict, display_name=None, palette=None, custom_css=None, badges=None):
        self.variables = variables

        if display_name:
            self.display_name = display_name

        if palette:
            self.palette = palette

        if custom_css:
            self.custom_css = custom_css

        if badges:
            self.badges = badges

    def new_from_path(self, preset_path: str):
        self.preset_path = preset_path

        try:
            with open(self.preset_path, "r", encoding="utf-8") as file:
                preset_text = file.read()
                file.close()
        except OSError as e:
            logging.error(f"Failed to read contents of a preset in location: {self.preset_path}.", exc=e)
            raise

        try:
            preset = json.loads(preset_text)
        except json.JSONDecodeError as e:
            logging.error("Error while decoding JSON data.", exc=e)
            raise

        self.__load_values(preset)

        return self

    def new_from_resource(self, text: str):
        preset_text = text

        try:
            preset = json.loads(preset_text)
        except json.JSONDecodeError as e:
            logging.error("Error while decoding JSON data.", exc=e)
            raise

        self.__load_values(preset)

        return self

    def new_from_dict(self, preset: dict):
        self.__load_values(preset)

        return self

    def __load_values(self, preset):
        try:
            self.display_name = preset["name"]
            self.variables = preset["variables"]
            self.palette = preset["palette"]

            if "badges" in preset:
                self.badges = preset["badges"]
            else:
                self.badges = {}

            if "custom_css" in preset:
                self.custom_css = preset["custom_css"]
            else:
                for app_type in custom_css_gtk_versions:
                    self.custom_css[app_type] = ""
        except Exception as e:
            logging.error("Failed to create a new preset object.", exc=e)
            raise

    # Rename an existing preset
    def rename(self, name):
        self.display_name = name
        old_path = self.preset_path
        self.preset_path = os.path.join(
            os.path.dirname(self.preset_path), to_slug_case(name) + ".json"
        )

        self.save_to_file(to=self.preset_path)
        os.remove(old_path)

    def get_preset_json(self, indent=None):
        preset_dict = {
            "name": self.display_name,
            "variables": self.variables,
            "palette": self.palette,
            "custom_css": self.custom_css,
            "plugins": self.plugins_list
        }

        json_output = json.dumps(preset_dict, indent=indent)

        return json_output

    # Save a new user preset (or overwrite one)
    def save_to_file(self, name=None, plugins_list=None, to=None):
        self.display_name = name if name else self.display_name

        if to is None:
            filename = to_slug_case(name) if name else to_slug_case(self.display_name)
            self.preset_path = os.path.join(
                presets_dir, "user", filename + ".json"
            )
        else:
            self.preset_path = to

        if not os.path.exists(os.path.join(presets_dir, "user")):
            try:
                os.makedirs(os.path.join(presets_dir, "user"))
            except OSError as e:
                logging.error("Failed to create a new preset directory.", exc=e)
                raise

        if plugins_list:
            plugins_list = plugins_list.save()

        try:
            with open(self.preset_path, "w", encoding="utf-8") as file:
                content = self.get_preset_json(indent=4)
                file.write(content)
                file.close()
        except OSError as e:
            logging.error("Failed to save preset as a file.", exc=e)
            raise

    # TODO: Add validation
    def validate(self):
        return True
