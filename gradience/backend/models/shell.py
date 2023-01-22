# shell.py
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
import re
import shutil

import material_color_utilities_python as monet

from gi.repository import Gio, GLib

from gradience.backend.utils.common import to_slug_case
from gradience.backend.constants import datadir

from gradience.backend.logger import Logger

logging = Logger(logger_name="ShellTheme")


class ShellTheme:
    # Supported GNOME Shell versions: 42, 43
    shell_versions = [42, 43]
    version_target = None

    variables = {}
    custom_colors = {}
    custom_css = None

    def __init__(self, shell_version: int):
        if shell_version in self.shell_versions:
            self.version_target = shell_version
        else:
            # TODO: Create custom exception for theming related errors
            raise Exception(f"GNOME Shell version {shell_version} not in range [42, 43]")

        self.user_theme_schema = "org.gnome.shell.extensions.user-theme"
        self.settings = Gio.Settings.new(self.user_theme_schema)

        # Theme source/output paths
        self.templates_dir = os.path.join(datadir, "gradience", "shell", "templates", str(self.version_target))
        self.colors_template = os.path.join(self.templates_dir, "colors.template")
        self.switches_template = os.path.join(self.templates_dir, "switches.template")
        self.main_template = os.path.join(self.templates_dir, "gnome-shell.template")

        self.theme_source = os.path.join(datadir, "gradience", "shell", str(self.version_target))
        self.colors_source = os.path.join(self.theme_source, "gnome-shell-sass", "_colors.scss")
        self.switches_source = os.path.join(self.theme_source, "gnome-shell-sass", "widgets", "_switches.scss")
        self.main_source = os.path.join(self.theme_source, "gnome-shell.scss")

        self.switch_on_source = os.path.join(self.theme_source, "toggle-on.svg")
        self.switch_off_source = os.path.join(self.theme_source, "toggle-off.svg")

        self.theme_output = os.path.join(GLib.get_home_dir(), ".local/share/themes", "gradience-shell", "gnome-shell")
        self.assets_output = os.path.join(self.theme_output, "assets")

    def create_theme(self, preset_obj):
        self.variables = preset_obj.variables

        self.insert_variables()

        if not os.path.exists(self.theme_output):
            try:
                dirs = Gio.File.new_for_path(self.theme_output)
                dirs.make_directory_with_parents(None)
            except GLib.GError as e:
                logging.error(f"Unable to create directories.", exc=e)
                raise

        self.compile_sass(os.path.join(self.theme_source, "gnome-shell.scss"),
            os.path.join(self.theme_output, "gnome-shell.css")
        )

        self.color_assets()
        self.set_shell_theme()

    def insert_variables(self):
        logging.debug(self.colors_source)

        #hexcode_regex = re.compile(r".*#[0-9a-f]+")
        template_regex = re.compile(r"{{(.*?)}}")

        colors_content = ""

        with open(self.colors_template, "r", encoding="utf-8") as template:
            for line in template:
                template_match = re.search(template_regex, line)
                if template_match != None:
                    key = template_match.__getitem__(1)
                    inserted = line.replace("{{" + key + "}}", self.variables[key])
                    colors_content += inserted
                else:
                    colors_content += line
            template.close()

        logging.debug(f"colors_content: {colors_content}")

        with open(self.colors_source, "w", encoding="utf-8") as sheet:
            sheet.write(colors_content)
            sheet.close()

    def compile_sass(self, sass_path, output_path):
        try:
            # TODO: Check where sassc is installed
            Gio.Subprocess.new(["/usr/bin/sassc", sass_path, output_path], Gio.SubprocessFlags.NONE)
        except GLib.GError as e:
            logging.error(f"Failed to compile SCSS source files using external sassc program.", exc=e)

    # TODO: Add coloring for other assets
    def color_assets(self):
        accent_bg = self.variables["accent_bg_color"]

        switch_on_svg = ""

        shutil.copy(self.switches_template, self.switches_source)

        with open(self.switch_on_source, "r", encoding="utf-8") as svg_data:
            switch_on_svg = svg_data.read()
            switch_on_svg = switch_on_svg.replace("fill:#3584e4", f"fill:{accent_bg}")
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

        shutil.copy(self.switch_on_source, os.path.join(self.assets_output, "toggle-on.svg"))
        shutil.copy(self.switch_off_source, os.path.join(self.assets_output, "toggle-off.svg"))

    def set_shell_theme(self):
        # Set default theme
        self.settings.set_string("name", "")

        # Set theme generated by Gradience
        self.settings.set_string("name", "gradience-shell")
