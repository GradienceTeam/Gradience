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

import os
import json
from pathlib import Path

from gi.repository import GLib, Gio

from gradience.backend.theming.monet import Monet
from gradience.backend.models.preset import Preset
from gradience.backend.utils.colors import rgba_from_argb

from gradience.backend.globals import presets_dir, get_gtk_theme_dir

from gradience.backend.logger import Logger

logging = Logger()


class PresetUtils:
    def __init__(self):
        self.preset = Preset()

    def generate_gtk_css(self, app_type: str, preset: Preset) -> str:
        variables = preset.variables
        palette = preset.palette
        custom_css = preset.custom_css

        final_css = ""

        for key in variables.keys():
            final_css += f"@define-color {key} {variables[key]};\n"

        for prefix_key in palette.keys():
            for key in palette[prefix_key].keys():
                final_css += f"@define-color {prefix_key + key} {palette[prefix_key][key]};\n"

        final_css += custom_css.get(app_type, "")

        return final_css

    def new_preset_from_monet(self, name=None, monet_palette=None, props=None, obj_only=False) -> Preset or None:
        if props:
            tone = props[0]
            theme = props[1]
        else:
            raise AttributeError("Properties 'tone' and/or 'theme' missing")

        if not monet_palette:
            raise AttributeError("Property 'monet_palette' missing")

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

        if obj_only == False and not name:
            raise AttributeError("You either need to set 'obj_only' property to True, or add value to 'name' property")

        if obj_only:
            if name:
                logging.debug("with name, obj_only")
                self.preset.new(variables=variable, display_name=name)
            else:
                logging.debug("no name, obj_only")
                self.preset.new(variables=variable)
            return self.preset

        if obj_only == False:
            logging.debug("no obj_only, name")
            self.preset.new(variables=variable, display_name=name)

            try:
                self.preset.save_to_file()
            except OSError:
                raise

    def get_presets_list(self, repo=None, full_list=False) -> dict:
        presets_list = {}

        def get_repo_presets(repo):
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
                            logging.error(f"Failed to load preset information.", exc=e)
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
                        logging.error(f"Failed to load preset information.", exc=e)
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
                get_repo_presets(repo)
            return presets_list
        elif repo:
            get_repo_presets(repo)
            return presets_list
        else:
            raise AttributeError("You either need to set 'repo' property, or change 'full_list' property to True")

    def apply_preset(self, app_type: str, preset: Preset) -> None:
        if app_type == "gtk4":
            theme_dir = get_gtk_theme_dir(app_type)

            if not os.path.exists(theme_dir):
                os.makedirs(theme_dir)

            gtk4_css = self.generate_gtk_css("gtk4", preset)
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

            gtk3_css = self.generate_gtk_css("gtk3", preset)
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
            logging.error(f"Unable to restore Gtk4 backup.", exc=e)
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
                logging.error(f"Unable to delete current preset.", exc=e)
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
                logging.error(f"Unable to delete current preset.", exc=e)
                raise
