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

from gi.repository import Gio

from gradience.backend.utils.common import extract_version, run_command


def get_shell_version():
    stdout = run_command(["gnome-shell", "--version"],
        get_stdout_text=True,
        allow_escaping=True).replace("\n", "")

    shell_version = extract_version(stdout, "GNOME Shell")

    return shell_version

def get_full_shell_version():
    stdout = run_command(["gnome-shell", "--version"],
        get_stdout_text=True,
        allow_escaping=True).replace("\n", "")

    shell_version = stdout[12:]

    return shell_version
