# shell.py
#
# Change the look of Adwaita, with ease
# Copyright (C) 2023, Gradience Team
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
import re
import shutil
import os.path
import sass

from gi.repository import GObject, Gio, GLib

from gradience.backend.models.preset import Preset
from gradience.backend.utils.colors import color_vars_to_color_code
from gradience.backend.utils.gnome import get_shell_version, get_shell_colors
from gradience.backend.utils.gsettings import GSettingsSetting, FlatpakGSettings, GSettingsMissingError
from gradience.backend.constants import datadir

from gradience.backend.logger import Logger
from gradience.backend.exceptions import UnsupportedShellVersion
from gradience.backend.globals import is_sandboxed

logging = Logger(logger_name="ShellTheme")


class ShellTheme:
    # Supported GNOME Shell versions: 42, 43, 44
    shell_versions = [42, 43, 44, 45]
    shell_versions_str = ", ".join(map(str, shell_versions))
    version_target = None

    theme_variant = None

    shell_colors = {}

    preset_variables = {}
    preset_palette = {}

    custom_css = None

    def __init__(self, shell_version=None):
        self._cancellable = Gio.Cancellable()

        if not shell_version:
            self._detect_shell_version()
        elif shell_version and shell_version in self.shell_versions:
            self.version_target = shell_version
        else:
            raise UnsupportedShellVersion(
                f"GNOME Shell version {shell_version} is not supported. (Supported versions: {self.shell_versions_str})")

        self.THEME_GSETTINGS_SCHEMA_ID = "org.gnome.shell.extensions.user-theme"
        self.THEME_GSETTINGS_SCHEMA_PATH = "/org/gnome/shell/extensions/user-theme/"
        self.THEME_GSETTINGS_SCHEMA_KEY = "name"

        self.THEME_EXT_NAME = "user-theme@gnome-shell-extensions.gcampax.github.com"
        self.THEME_GSETTINGS_DIR = os.path.join(GLib.get_home_dir(), ".local/share/",
            "gnome-shell", "extensions", self.THEME_EXT_NAME, "schemas")

        try:
            settings_retriever = FlatpakGSettings if is_sandboxed() else GSettingsSetting
            schema_dir = self.THEME_GSETTINGS_DIR if os.path.exists(self.THEME_GSETTINGS_DIR) else None
            self.settings = settings_retriever(self.THEME_GSETTINGS_SCHEMA_ID, schema_dir=schema_dir)
        except (GSettingsMissingError, GLib.GError):
            raise

        version_target_str = str(self.version_target)
        # Theme source/output paths
        self.templates_dir = os.path.join(datadir, "gradience", "shell", "templates", version_target_str)
        self.source_dir = os.path.join(GLib.get_home_dir(), ".cache", "gradience", "gradience-shell", version_target_str)

        if os.path.exists(self.source_dir):
            shutil.rmtree(self.source_dir)

        # Copy shell theme source directories to ~/.cache/gradience/gradience-shell
        shutil.copytree(
            os.path.join(datadir, "gradience", "shell", version_target_str),
            self.source_dir, dirs_exist_ok=True
        )

        # TODO: Allow user to use different name than "gradience-shell" (also, with default name, we should append "-light" suffix when generated from light preset)
        self.output_dir = os.path.join(GLib.get_home_dir(), ".local/share/themes", "gradience-shell", "gnome-shell")

        self.main_template = os.path.join(self.templates_dir, "gnome-shell.template")
        self.colors_template = os.path.join(self.templates_dir, "colors.template")
        self.palette_template = os.path.join(self.templates_dir, "palette.template")
        self.switches_template = os.path.join(self.templates_dir, "switches.template")

        self.main_source = os.path.join(self.source_dir, "gnome-shell.scss")
        self.colors_source = os.path.join(self.source_dir, "gnome-shell-sass", "_colors.scss")
        self.palette_source = os.path.join(self.source_dir, "gnome-shell-sass", "_palette.scss")
        self.switches_source = os.path.join(self.source_dir, "gnome-shell-sass", "widgets", "_switches.scss")

        self.assets_output = os.path.join(self.output_dir, "assets")

    def get_cancellable(self) -> Gio.Cancellable:
        return self._cancellable

    def apply_theme_async(self, caller:GObject.Object, callback:callable,
                            theme_variant:str,
                            preset: Preset):
        task = Gio.Task.new(caller, None, callback, self._cancellable)
        self.async_data = (theme_variant, preset)

        task.set_return_on_cancel(True)
        task.run_in_thread(self._apply_theme_thread)

    def _apply_theme_thread(self, task:Gio.Task, source_object:GObject.Object,
                                task_data:object,
                                cancellable:Gio.Cancellable):
        if task.return_error_if_cancelled():
            return

        theme_variant, preset = self.async_data

        output = self.apply_theme(source_object, theme_variant, preset)
        task.return_value(output)

    # TODO: Make it accept either dict or callable in `parent` parameter
    def apply_theme(self, parent: callable, theme_variant: str, preset: Preset):
        if theme_variant in ("light", "dark"):
            self.theme_variant = theme_variant
        else:
            raise ValueError(
                f"Theme variant {theme_variant} not in list: [light, dark]")

        try:
            self._create_theme(parent, preset)
        except (OSError, GLib.GError) as e:
            raise

    def _create_theme(self, parent: callable, preset: Preset):
        # Convert GTK color variables to normal color values
        self.preset_variables = color_vars_to_color_code(preset.variables, preset.palette)
        self.preset_palette = preset.palette
        self.custom_css = preset.custom_css

        # TODO: Move custom Shell colors list to Shell modules
        self.shell_colors = parent.shell_colors if parent != None else None

        self._insert_variables()
        self._recolor_assets()

        os.makedirs(self.output_dir, exist_ok=True)

        self._compile_sass(self.main_source,
            os.path.join(self.output_dir, "gnome-shell.css"))

        self._set_shell_theme()

    def _insert_variables(self):
        # hexcode_regex = re.compile(r".*#[0-9a-f]{3,6}")
        template_regex = re.compile(r"{{(.*?)}}")

        palette_content = ""

        with open(self.palette_template, "r", encoding="utf-8") as template:
            for line in template:
                if template_match := template_regex.search(line):
                    _key = template_match.__getitem__(1)
                    prefix, key = _key.split("_")[:2]
                    line = line.replace("{{" + _key + "}}", self.preset_palette[prefix + '_'][key])
                palette_content += line

        with open(self.palette_source, "w", encoding="utf-8") as sheet:
            sheet.write(palette_content)

        colors_content = ""

        with open(self.colors_template, "r", encoding="utf-8") as template:
            for line in template:
                if template_match := template_regex.search(line):
                    key = template_match.__getitem__(1)
                    shell_colors = self.shell_colors or get_shell_colors(self.preset_variables)
                    value = shell_colors.get(key) or self.preset_variables.get(key)
                    if value:
                        line = line.replace("{{" + key + "}}", value)
                colors_content += line

        with open(self.colors_source, "w", encoding="utf-8") as sheet:
            sheet.write(colors_content)

        main_content = ""

        with open(self.main_template, "r", encoding="utf-8") as template:
            key = "theme_variant"

            for line in template:
                if key in line:
                    value = f"'{self.theme_variant}'"
                    line = line.replace("{{" + key + "}}", value)
                elif "custom_css" in line:
                    key = "custom_css"
                    # Empty string when there is no custom CSS
                    value = self.custom_css.get('shell', "")
                    line = line.replace("{{" + key + "}}", value)
                main_content += line

        with open(self.main_source, "w", encoding="utf-8") as sheet:
            sheet.write(main_content)

    def _compile_sass(self, sass_path, output_path):
        try:
            compiled = sass.compile(filename=sass_path, output_style="nested")
        except (GLib.GError, sass.CompileError) as e:
            logging.error(
                f"Failed to compile SCSS source files.", exc=e)
        else:
            with open(output_path, "w", encoding="utf-8") as css_file:
                css_file.write(compiled)

    # TODO: Add recoloring for other assets
    def _recolor_assets(self):
        accent_bg = self.preset_variables["accent_bg_color"]

        switch_on_source = os.path.join(self.source_dir, "toggle-on.svg")

        shutil.copy(
            self.switches_template,
            self.switches_source
        )

        with open(switch_on_source, "r", encoding="utf-8") as svg_data:
            switch_on_svg = svg_data.read()
            switch_on_svg = switch_on_svg.replace(
                "fill:#3584e4", f"fill:{accent_bg}")

        with open(switch_on_source, "w", encoding="utf-8") as svg_data:
            svg_data.write(switch_on_svg)

        os.makedirs(self.assets_output, exist_ok=True)

        shutil.copy(
            switch_on_source,
            os.path.join(self.assets_output, "toggle-on.svg")
        )

    def _set_shell_theme(self):
        key = self.THEME_GSETTINGS_SCHEMA_KEY

        # Set default theme
        self.settings.reset(key)

        if is_sandboxed():
            # Set theme generated by Gradience
            self.settings.set(key, "gradience-shell")
        else:
            # Set theme generated by Gradience
            self.settings.set_string(key, "gradience-shell")

    def _detect_shell_version(self):
        shell_ver = get_shell_version()

        if shell_ver.startswith("3"):
            raise UnsupportedShellVersion(
                f"GNOME Shell version {shell_ver} is not supported. (Supported versions: {self.shell_versions_str})")

        if shell_ver.startswith("4"):
            shell_ver = int(shell_ver[:2])

            if shell_ver in self.shell_versions:
                self.version_target = shell_ver
            else:
                raise UnsupportedShellVersion(
                    f"GNOME Shell version {shell_ver} is not supported. (Supported versions: {self.shell_versions_str})")

    def reset_theme_async(self, caller:GObject.Object, callback:callable):
        task = Gio.Task.new(caller, None, callback, self._cancellable)

        task.set_return_on_cancel(True)
        task.run_in_thread(self._reset_theme_thread)

    def reset_theme(self):
        key = self.THEME_GSETTINGS_SCHEMA_KEY

        # Set default theme
        self.settings.reset(key)

    def _reset_theme_thread(self, task:Gio.Task, source_object:GObject.Object,
                task_data:object, cancellable:Gio.Cancellable):
        if task.return_error_if_cancelled():
            return

        output = self.reset_theme()
        task.return_value(output)
