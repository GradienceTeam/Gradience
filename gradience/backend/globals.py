# globals.py
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

from gi.repository import Xdp

from gradience.backend import constants


presets_dir = os.path.join(
    os.environ.get("XDG_CONFIG_HOME", os.environ["HOME"] + "/.config"),
    "presets"
)

preset_repos = {
    "Official": "https://github.com/GradienceTeam/Community/raw/next/official.json",
    "Curated": "https://github.com/GradienceTeam/Community/raw/next/curated.json"
}

user_plugin_dir = os.path.join(
    os.environ.get("XDG_DATA_HOME", os.environ["HOME"] + "/.local/share"),
    "gradience",
    "plugins"
)

system_plugin_dir = os.path.join(
    constants.pkgdatadir,
    "plugins"
)

def get_gtk_theme_dir(app_type):
    if app_type == "gtk4":
        theme_dir = os.path.join(
            os.environ.get("XDG_CONFIG_HOME",
                            os.environ["HOME"] + "/.config"),
            "gtk-4.0"
        )
    elif app_type == "gtk3":
        theme_dir = os.path.join(
            os.environ.get("XDG_CONFIG_HOME",
                            os.environ["HOME"] + "/.config"),
            "gtk-3.0"
        )

    return theme_dir

def is_sandboxed():
    portal = Xdp.Portal()

    is_sandboxed = portal.running_under_sandbox()

    return is_sandboxed

def get_available_sassc():
    pass
