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

import os
import json

from pathlib import Path

from gi.repository import GLib, Gio

from gradience.backend.models.preset import Preset

from gradience.backend.utils.colors import argb_to_color_code
from gradience.backend.utils.theming import generate_gtk_css
from gradience.backend.globals import presets_dir, get_gtk_theme_dir

from gradience.backend.logger import Logger

logging = Logger()


class PresetUtils:
    def __init__(self):
        pass

    def get_presets_list(self, repo=None, full_list=False) -> dict:
        presets_list = {}

        def __get_repo_presets(repo):
            if repo.is_dir():
                for file_name in repo.iterdir():
                    file_name = str(file_name)
                    if file_name.endswith(".json"):
                        try:
                            with open(
                                os.path.join(presets_dir, file_name),
                                "r",
                                encoding="utf-8",
                            ) as file:
                                preset_text = file.read()
                                file.close()
                        except (OSError, KeyError) as e:
                            logging.error("Failed to load preset information.", exc=e)
                            raise
                        else:
                            preset = json.loads(preset_text)
                            if preset.get("variables") is None:
                                raise KeyError("'variables' section missing in loaded preset file")
                            if preset.get("palette") is None:
                                raise KeyError("'palette' section missing in loaded preset file")
                            presets_list[file_name] = preset[
                                "name"
                            ]
            elif repo.is_file():
                # this exists to keep compatibility with old presets
                if repo.name.endswith(".json"):
                    logging.warning("Legacy preset found. Moving to new structure.")

                    try:
                        if not os.path.isdir(os.path.join(presets_dir, "user")):
                            os.mkdir(os.path.join(presets_dir, "user"))

                        os.rename(repo, os.path.join(
                            presets_dir, "user", repo.name))

                        with open(
                            os.path.join(presets_dir, "user", repo),
                            "r",
                            encoding="utf-8",
                        ) as file:
                            preset_text = file.read()
                            file.close()
                    except (OSError, KeyError) as e:
                        logging.error("Failed to load preset information.", exc=e)
                        raise
                    else:
                        preset = json.loads(preset_text)
                        if preset.get("variables") is None:
                            raise KeyError("'variables' section missing in loaded preset file")
                        if preset.get("palette") is None:
                            raise KeyError("'palette' section missing in loaded preset file")
                        presets_list["user"][file_name] = preset[
                            "name"
                        ]

        if full_list:
            for repo in Path(presets_dir).iterdir():
                logging.debug(f"presets_dir.iterdir: {repo}")
                __get_repo_presets(repo)
            return presets_list
        elif repo:
            __get_repo_presets(repo)
            return presets_list
        else:
            raise AttributeError("You either need to set 'repo' property, or change 'full_list' property to True")

    def apply_preset(self, app_type: str, preset: Preset) -> None:
        if app_type == "gtk4":
            theme_dir = get_gtk_theme_dir(app_type)

            if not os.path.exists(theme_dir):
                os.makedirs(theme_dir)

            gtk4_css = generate_gtk_css("gtk4", preset)
            contents = ""

            try:
                with open(
                    os.path.join(theme_dir, "gtk.css"), "r", encoding="utf-8"
                ) as file:
                    contents = file.read()
            except FileNotFoundError: # first run
                pass
            else:
                with open(
                    os.path.join(theme_dir, "gtk.css.bak"), "w", encoding="utf-8"
                ) as file:
                    file.write(contents)
            finally:
                with open(
                    os.path.join(theme_dir, "gtk.css"), "w", encoding="utf-8"
                ) as file:
                    file.write(gtk4_css)
        elif app_type == "gtk3":
            theme_dir = get_gtk_theme_dir(app_type)

            if not os.path.exists(theme_dir):
                os.makedirs(theme_dir)

            gtk3_css = generate_gtk_css("gtk3", preset)
            contents = ""

            try:
                with open(
                    os.path.join(theme_dir, "gtk.css"), "r", encoding="utf-8"
                ) as file:
                    contents = file.read()
            except FileNotFoundError: # first run
                pass
            else:
                with open(
                    os.path.join(theme_dir, "gtk.css.bak"), "w", encoding="utf-8"
                ) as file:
                    file.write(contents)
            finally:
                with open(
                    os.path.join(theme_dir, "gtk.css"), "w", encoding="utf-8"
                ) as file:
                    file.write(gtk3_css)

    def restore_gtk4_preset(self) -> None:
        try:
            with open(
                os.path.join(
                    os.environ.get(
                        "XDG_CONFIG_HOME", os.environ["HOME"] +
                        "/.config"
                    ),
                    "gtk-4.0/gtk.css.bak",
                ),
                "r",
                encoding="utf-8",
            ) as backup:
                contents = backup.read()
                backup.close()

            with open(
                os.path.join(
                    os.environ.get(
                        "XDG_CONFIG_HOME", os.environ["HOME"] +
                        "/.config"
                    ),
                    "gtk-4.0/gtk.css",
                ),
                "w",
                encoding="utf-8",
            ) as gtk4css:
                gtk4css.write(contents)
                gtk4css.close()
        except OSError as e:
            logging.error("Unable to restore Gtk4 backup.", exc=e)
            raise

    def reset_preset(self, app_type: str) -> None:
        if app_type == "gtk4":
            file = Gio.File.new_for_path(
                os.path.join(
                    os.environ.get(
                        "XDG_CONFIG_HOME", os.environ["HOME"] + "/.config"
                    ),
                    "gtk-4.0/gtk.css",
                )
            )

            try:
                file.delete()
            except GLib.GError as e:
                logging.error("Unable to delete current preset.", exc=e)
                raise
        elif app_type == "gtk3":
            file = Gio.File.new_for_path(
                os.path.join(
                    os.environ.get(
                        "XDG_CONFIG_HOME", os.environ["HOME"] + "/.config"
                    ),
                    "gtk-3.0/gtk.css",
                )
            )

            try:
                file.delete()
            except GLib.GError as e:
                logging.error("Unable to delete current preset.", exc=e)
                raise
