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

import material_color_utilities_python as monet

from gi.repository import Gio, GLib

from gradience.backend.constants import datadir
from gradience.backend.models.preset import Preset
from gradience.backend.utils.common import to_slug_case

from gradience.backend.logger import Logger

logging = Logger(logger_name="ShellTheme")


SHELL_SCHEMA = "org.gnome.shell.extensions.user-theme"

#try:
settings = Gio.Settings.new(SHELL_SCHEMA)
'''except GLib.GError as e:
    logging.critical(f"Settings schema for User Themes shell extension couldn't be loaded. Make sure you downloaded an extension before applying shell theme.", exc=e)
'''


class ShellTheme:
    # Supported GNOME Shell versions: 42, 43
    shell_versions = [42, 43]
    version = None

    variables = {}
    custom_colors = {}
    custom_css = None

    def __init__(self, shell_version: int):
        if shell_version in self.shell_versions:
            self.version = shell_version
        else:
            # TODO: Create custom exception for theming related errors
            raise Exception(f"GNOME Shell version {shell_version} not in range [42, 43]")

        self.templates_dir = os.path.join(datadir, "gradience", "shell", "templates", str(self.version))
        self.colors_template = os.path.join(self.templates_dir, "colors.template")
        self.main_template = os.path.join(self.templates_dir, "gnome-shell.template")

        self.theme_source = os.path.join(datadir, "gradience", "shell", str(self.version))
        self.colors_source = os.path.join(self.theme_source, "gnome-shell-sass", "_colors.scss")
        self.main_source = os.path.join(self.theme_source, "gnome-shell.scss")

        self.theme_output = os.path.join(GLib.get_home_dir(), ".local/share/themes", "gradience-shell", "gnome-shell")

    def create_theme(self, preset: Preset):
        self.variables = preset.variables

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

        self.set_theme()

    def insert_variables(self):
        logging.debug(self.colors_source)

        #hexcode_regex = r"\$_dark_base_color: .*#[0-9a-f]+"
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

        print(colors_content)

        with open(self.colors_source, "w", encoding="utf-8") as sheet:
            sheet.write(colors_content)
            sheet.close()

        # TODO: Repurpose this snippet later
        '''main_content = ""

        with open(self.main_template, "r", encoding="utf-8") as template:
            for line in template:
                template_match = re.search(template_regex, line)
                if template_match != None:
                    key = template_match.__getitem__(1)
                    inserted = line.replace("{{" + key + "}}", self.theme_type)
                    main_content += inserted
                else:
                    main_content += line
            template.close()

        print(main_content)

        with open(self.main_source, "w", encoding="utf-8") as sheet:
            sheet.write(main_content)
            sheet.close()'''

    def compile_sass(self, sass_path, output_path):
        try:
            Gio.Subprocess.new(["/usr/bin/sassc", sass_path, output_path], Gio.SubprocessFlags.NONE)
        except GLib.GError as e:
            logging.error(f"Failed to compile SCSS files using external sassc program.", exc=e)

    def set_theme(self):
        # Set default theme
        settings.set_string("name", "")

        # Set theme generated by Gradience
        settings.set_string("name", "gradience-shell")
