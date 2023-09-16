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

from gradience.backend.utils.theming import generate_gtk_css
from gradience.backend.globals import user_config_dir, presets_dir, get_gtk_theme_dir, is_sandboxed
from gradience.backend.utils.gsettings import GSettingsSetting, FlatpakGSettings, GSettingsMissingError

from gradience.backend.logger import Logger

logging = Logger()


class PresetUtils:
    THEME_GSETTINGS_SCHEMA_ID = "org.gnome.desktop.interface"
    
    def __init__(self):
        pass

    def set_gtk3_theme(self):
        settings_retriever = FlatpakGSettings if is_sandboxed() else GSettingsSetting
        self.settings = settings_retriever(self.THEME_GSETTINGS_SCHEMA_ID, schema_dir=None)
        self.settings.set_string("gtk-theme", "adw-gtk3")

    def get_presets_list(self, repo=None, full_list=False) -> dict:
        presets_list = {}

        def __get_repo_presets(repo):
            if repo.is_dir():
                for file_name in repo.iterdir():
                    file_name = str(file_name)
                    if file_name.endswith(".json"):
                        try:
                            with open(os.path.join(presets_dir, file_name), "r", encoding="utf-8") as file:
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

                            presets_list[file_name] = preset["name"]
            elif repo.is_file():
                # this exists to keep compatibility with old preset structure
                if repo.name.endswith(".json"):
                    logging.warning("Legacy preset structure found. Moving to a new structure.")

                    try:
                        if not os.path.isdir(os.path.join(presets_dir, "user")):
                            os.mkdir(os.path.join(presets_dir, "user"))

                        os.rename(repo, os.path.join(
                            presets_dir, "user", repo.name))

                        with open(os.path.join(presets_dir, "user", repo), "r", encoding="utf-8") as file:
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

                        presets_list["user"][file_name] = preset["name"]

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
        theme_dir = get_gtk_theme_dir(app_type)
        gtk_css_path = os.path.join(theme_dir, "gtk.css")

        if app_type == "gtk3":
            self.set_gtk3_theme()

        if not os.path.exists(theme_dir):
            os.makedirs(theme_dir)

        try:
            with open(gtk_css_path, "r", encoding="utf-8") as css_file:
                contents = css_file.read()
                css_file.close()
        except FileNotFoundError:
            logging.warning(f"gtk.css file not found in {gtk_css_path}. Generating new stylesheet.")
        else:
            with open(gtk_css_path + ".bak", "w", encoding="utf-8") as backup:
                backup.write(contents)
                backup.close()
        finally:
            with open(gtk_css_path, "w", encoding="utf-8") as css_file:
                css_file.write(generate_gtk_css(app_type, preset))
                css_file.close()

    def restore_preset(self, app_type: str) -> None:
        theme_dir = get_gtk_theme_dir(app_type)
        gtk_css_path = os.path.join(theme_dir, "gtk.css")

        try:
            with open(gtk_css_path + ".bak", "r", encoding="utf-8") as backup:
                contents = backup.read()
                backup.close()

            with open(gtk_css_path, "w", encoding="utf-8") as css_file:
                css_file.write(contents)
                css_file.close()
        except OSError as e:
            logging.error(f"Unable to restore {app_type.capitalize()} preset backup.", exc=e)
            raise

    def reset_preset(self, app_type: str) -> None:
        theme_dir = get_gtk_theme_dir(app_type)
        gtk_css_path = os.path.join(theme_dir, "gtk.css")

        file = Gio.File.new_for_path(gtk_css_path)

        try:
            file.delete()
        except GLib.GError as e:
            if e.code == 1:
                return

            logging.error("Unable to delete current preset.", exc=e)
            raise
