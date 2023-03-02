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
import xml.dom.minidom
import gettext

from gi.repository import Gio, GLib

from gradience.backend.models.preset import Preset
from gradience.backend.utils.shell import get_shell_version
from gradience.backend.constants import datadir
from gradience.backend.utils.gsettings import GSettingsSetting

from gradience.backend.logger import Logger
from gradience.backend.exceptions import UnsupportedShellVersion

logging = Logger(logger_name="ShellTheme")


shell_to_adw = {
    "_dark_base_color": "window_bg_color",
    "fg_color": "window_fg_color",
    "selected_fg_color": "accent_fg_color",
    "selected_bg_color": "accent_bg_color",
    "osd_fg_color": "accent_fg_color"
}


class ShellTheme:
    # Supported GNOME Shell versions: 42, 43, 44
    shell_versions = [42, 43, 44]
    shell_versions_str = [str(version) for version in shell_versions]
    version_target = None

    variant = None
    variables = {}
    palette = {}
    custom_colors = {}
    custom_css = None

    def __init__(self, shell_version=None):
        if not shell_version:
            self.detect_shell_version()
        elif shell_version and shell_version in self.shell_versions:
            self.version_target = shell_version
        else:
            raise UnsupportedShellVersion(
                f"GNOME Shell version {shell_version} is not supported. (Supported versions: {', '.join(self.shell_versions_str)})")

        self.user_theme_schema = "org.gnome.shell.extensions.user-theme"
        self.THEME_EXT_NAME = "user-theme@gnome-shell-extensions.gcampax.github.com"
        self.THEME_GSETTINGS_SCHEMA = "org.gnome.shell.extensions.user-theme"
        self.THEME_GSETTINGS_NAME = "name"
        self.THEME_GSETTINGS_DIR = os.path.join(GLib.get_user_data_dir(),
            "gnome-shell", "extensions", self.THEME_EXT_NAME, "schemas")

        # try:
        if os.path.exists(self.THEME_GSETTINGS_DIR):
            self.settings = GSettingsSetting(self.THEME_GSETTINGS_SCHEMA,
                schema_dir=self.THEME_GSETTINGS_DIR)
        else:
            self.settings = GSettingsSetting(self.THEME_GSETTINGS_SCHEMA)

        name = self.settings.get_string(self.THEME_GSETTINGS_NAME)

        # Theme source/output paths
        self.templates_dir = os.path.join(datadir, "gradience", "shell", "templates", str(self.version_target))
        self.source_dir = os.path.join(GLib.get_home_dir(), ".cache", "gradience", "gradience-shell", str(self.version_target))

        if os.path.exists(self.source_dir):
            shutil.rmtree(self.source_dir)

        shutil.copytree(os.path.join(datadir, "gradience", "shell",
            str(self.version_target)), self.source_dir, dirs_exist_ok=True
        )

        self.output_dir = os.path.join(GLib.get_home_dir(), ".local/share/themes", "gradience-shell", "gnome-shell")

        self.main_template = os.path.join(self.templates_dir, "gnome-shell.template")
        self.colors_template = os.path.join(self.templates_dir, "colors.template")
        self.palette_template = os.path.join(self.templates_dir, "palette.template")
        # NOTE: From what I saw in some Shell themes, we can write our own Gresource schema, which will allow us to remove switches.template
        self.switches_template = os.path.join(self.templates_dir, "switches.template")

        self.main_source = os.path.join(self.source_dir, "gnome-shell.scss")
        self.colors_source = os.path.join(self.source_dir, "gnome-shell-sass", "_colors.scss")
        self.palette_source = os.path.join(self.source_dir, "gnome-shell-sass", "_palette.scss")
        self.switches_source = os.path.join(self.source_dir, "gnome-shell-sass", "widgets", "_switches.scss")

        self.switch_on_source = os.path.join(self.source_dir, "toggle-on.svg")
        self.switch_off_source = os.path.join(self.source_dir, "toggle-off.svg")

        self.assets_output = os.path.join(self.output_dir, "assets")

    def apply_theme(self, app, variant: str):
        if variant in ("light", "dark"):
            self.variant = variant
        else:
            raise ValueError(
                f"Theme variant {variant} not in list: [light, dark]")

        try:
            self.create_theme(app)
        except (OSError, GLib.GError) as e:
            raise

    def create_theme(self, app):
        preset = app.preset
        self.variables = preset.variables
        self.palette = preset.palette
        self.custom_css = preset.custom_css
        self.custom_colors = app.custom_colors

        self.insert_variables()

        if not os.path.exists(self.output_dir):
            try:
                dirs = Gio.File.new_for_path(self.output_dir)
                dirs.make_directory_with_parents(None)
            except GLib.GError as e:
                logging.error(f"Unable to create directories.", exc=e)
                raise

        self.compile_sass(os.path.join(self.source_dir, "gnome-shell.scss"),
            os.path.join(self.output_dir, "gnome-shell.css"))

        self.recolor_assets()
        self.set_shell_theme()

    def insert_variables(self):
        # hexcode_regex = re.compile(r".*#[0-9a-f]{3,6}")
        template_regex = re.compile(r"{{(.*?)}}")

        palette_content = ""

        with open(self.palette_template, "r", encoding="utf-8") as template:
            for line in template:
                template_match = re.search(template_regex, line)
                if template_match != None:
                    _key = template_match.__getitem__(1)
                    prefix = _key.split("_")[0] + "_"
                    key = _key.split("_")[1]
                    inserted = line.replace("{{" + _key + "}}", self.palette[prefix][key])
                    palette_content += inserted
                else:
                    palette_content += line
            template.close()

        with open(self.palette_source, "w", encoding="utf-8") as sheet:
            sheet.write(palette_content)
            sheet.close()

        colors_content = ""

        with open(self.colors_template, "r", encoding="utf-8") as template:
            for line in template:
                template_match = re.search(template_regex, line)
                if template_match != None:
                    key = template_match.__getitem__(1)
                    try:
                        inserted = line.replace(
                            "{{" + key + "}}", self.variables[key])
                    except KeyError:
                        inserted = line.replace(
                            "{{" + key + "}}", self.custom_colors[key])

                    colors_content += inserted
                else:
                    colors_content += line
            template.close()

        with open(self.colors_source, "w", encoding="utf-8") as sheet:
            sheet.write(colors_content)
            sheet.close()

        '''with open(self.colors_template, "r", encoding="utf-8") as template:
            for line in template:
                template_match = re.findall(template_regex, line)
                if template_match != None:
                    #key = template_match.__getitem__(1)
                    for key in template_match:
                        #inserted = re.sub(template_regex, self.variables[key], line)
                        #print(inserted)
                        inserted = line.replace("{{" + key + "}}", self.variables[key])
                        print(inserted)
                        colors_content += inserted
                else:
                    colors_content += line
            template.close()'''

        main_content = ""

        with open(self.main_template, "r", encoding="utf-8") as template:
            key = "theme_variant"

            for line in template:
                if key in line:
                    inserted = line.replace(
                        "{{" + key + "}}", f"'{self.variant}'")
                    main_content += inserted
                elif "custom_css" in line:
                    key = "custom_css"
                    try:
                        inserted = line.replace(
                            "{{" + key + "}}", self.custom_css['shell'])
                    except KeyError:  # No custom CSS
                        inserted = line.replace("{{" + key + "}}", "")
                    main_content += inserted
                else:
                    main_content += line
            template.close()

        with open(self.main_source, "w", encoding="utf-8") as sheet:
            sheet.write(main_content)
            sheet.close()

    def compile_sass(self, sass_path, output_path):
        try:
            # TODO: Check where sassc is installed
            Gio.Subprocess.new(
                ["/usr/bin/sassc", sass_path, output_path], Gio.SubprocessFlags.NONE)
        except GLib.GError as e:
            logging.error(
                f"Failed to compile SCSS source files using external sassc program.", exc=e)

    # TODO: Add recoloring for other assets
    def recolor_assets(self):
        accent_bg = self.variables["accent_bg_color"]

        shutil.copy(
            self.switches_template,
            self.switches_source
        )

        # TODO: Make asset templates, so that assets can be recolored more than once per install
        with open(self.switch_on_source, "r", encoding="utf-8") as svg_data:
            switch_on_svg = svg_data.read()
            switch_on_svg = switch_on_svg.replace(
                "fill:#3584e4", f"fill:{accent_bg}")
            svg_data.close()

        with open(self.switch_on_source, "w", encoding="utf-8") as svg_data:
            svg_data.write(switch_on_svg)
            svg_data.close()

        if not os.path.exists(self.assets_output):
            try:
                dirs = Gio.File.new_for_path(self.assets_output)
                dirs.make_directory_with_parents(None)
            except GLib.GError as e:
                logging.error(f"Unable to create directories.", exc=e)
                raise

        shutil.copy(
            self.switch_on_source,
            os.path.join(self.assets_output, "toggle-on.svg")
        )

        shutil.copy(
            self.switch_off_source,
            os.path.join(self.assets_output, "toggle-off.svg")
        )

    def set_shell_theme(self):
        # Set default theme
        self.settings.set_string("name", "")

        # Set theme generated by Gradience
        self.settings.set_string("name", "gradience-shell")

    def unset_shell_theme(self):
        # Set default theme
        self.settings.set_string("name", "")

    def detect_shell_version(self):
        shell_ver = get_shell_version()

        if shell_ver.startswith("3"):
            raise UnsupportedShellVersion(
                f"GNOME Shell version {shell_ver} is not supported. (Supported versions: {', '.join(self.shell_versions_str)})")

        if shell_ver.startswith("4"):
            shell_ver = int(shell_ver[:2])

            if shell_ver in self.shell_versions:
                self.version_target = shell_ver
            else:
                raise UnsupportedShellVersion(
                    f"GNOME Shell version {shell_ver} is not supported. (Supported versions: {', '.join(self.shell_versions_str)})")
