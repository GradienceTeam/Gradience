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

from gradience.backend.models.preset import Preset
from gradience.backend.utils.subprocess import GradienceSubprocess
from gradience.backend.utils.common import extract_version

# TODO: Remove this import later (imports from gradience.frontend are not allowed in backend)
from gradience.frontend.schemas.shell_schema import shell_schema


# TODO: Return failure if command was not found
def get_shell_version() -> str:
    cmd_list = ["gnome-shell", "--version"]
    process = GradienceSubprocess()

    completed = process.run(cmd_list, allow_escaping=True)
    stdout = process.get_stdout_data(completed, decode=True)

    shell_version = extract_version(stdout, "GNOME Shell")

    return shell_version

def get_full_shell_version() -> str:
    cmd_list = ["gnome-shell", "--version"]
    process = GradienceSubprocess()

    completed = process.run(cmd_list, allow_escaping=True)
    stdout = process.get_stdout_data(completed, decode=True)

    shell_version = stdout[12:]

    return shell_version

def is_gnome_available() -> bool:
    xdg_current_desktop = os.environ.get("XDG_CURRENT_DESKTOP").lower()

    if "gnome" in xdg_current_desktop:
        return True

    return False

def is_shell_ext_installed(uuid: str, check_enabled: bool = False) -> bool:
    """
    Checks if Shell extension with provided UUID from `uuid` parameter
    is installed in system.

    `check_enabled` parameter allows for checking if extension is enabled.
    """

    if check_enabled:
        cmd_list = ["gnome-extensions", "list", "--enabled"]
    else:
        cmd_list = ["gnome-extensions", "list"]

    process = GradienceSubprocess()

    completed = process.run(cmd_list, allow_escaping=True)
    stdout = process.get_stdout_data(completed, decode=True)

    ext_list = stdout.split("\n")
    if ext_list[-1] == "":
        ext_list.pop(-1)

    if uuid in ext_list:
        return True

    return False

def get_shell_colors(preset_variables: Preset.variables) -> dict:
    shell_colors = {}

    for variable in shell_schema["variables"]:
        shell_colors[variable["name"]] = variable["var_name"]

    for shell_key, var_name in shell_colors.items():
        if shell_key == "panel_bg_color":
            shell_colors[shell_key] = shell_schema["variables"][5]["default_value"]
            continue
        shell_colors[shell_key] = preset_variables[var_name]

    return shell_colors
