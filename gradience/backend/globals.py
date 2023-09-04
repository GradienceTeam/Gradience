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


user_config_dir = os.environ.get(
    "XDG_CONFIG_HOME", os.environ["HOME"] + "/.config"
)

user_data_dir = os.environ.get(
    "XDG_DATA_HOME", os.environ["HOME"] + "/.local/share"
)

user_cache_dir = os.environ.get(
    "XDG_CACHE_HOME", os.environ["HOME"] + "/.cache"
)

presets_dir = os.path.join(user_config_dir, "presets")

user_plugin_dir = os.path.join(user_data_dir, "gradience", "plugins")
system_plugin_dir = os.path.join(constants.pkgdatadir, "plugins")

preset_repos_github = {
    "Official": "https://github.com/GradienceTeam/Community/raw/next/official.json",
    "Curated": "https://github.com/GradienceTeam/Community/raw/next/curated.json"
}

preset_repos_jsdelivr = {
    "Official": "https://cdn.jsdelivr.net/gh/GradienceTeam/Community@next/official.json",
    "Curated": "https://cdn.jsdelivr.net/gh/GradienceTeam/Community@next/curated.json"
}

# preset_repos should be dynamically imported depending of user settings

# Adwaita named UI colors prefixes list
# NOTE: Remember to update this list if new libadwaita version brings up new variables
adw_variables_prefixes = [
    "accent_",
    "destructive_",
    "success_",
    "warning_",
    "error_",
    "window_",
    "view_",
    "headerbar_",
    "card_",
    "dialog_",
    "popover_",
    "shade_",
    "scrollbar_",
    "borders"
]

# Adwaita named palette colors prefixes list
# NOTE: Remember to update this list if new libadwaita version brings up new variables
adw_palette_prefixes = [
    "blue_",
    "green_",
    "yellow_",
    "orange_",
    "red_",
    "purple_",
    "brown_",
    "light_",
    "dark_"
]

def get_gtk_theme_dir(app_type: str):
    if app_type == "gtk4":
        theme_dir = os.path.join(user_config_dir, "gtk-4.0")

    if app_type == "gtk3":
        theme_dir = os.path.join(user_config_dir, "gtk-3.0")

    return theme_dir

def is_sandboxed():
    portal = Xdp.Portal()

    is_sandboxed = portal.running_under_sandbox()

    return is_sandboxed
