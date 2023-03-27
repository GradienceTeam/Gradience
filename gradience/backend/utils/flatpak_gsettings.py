# gsettings.py
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

from gi.repository import GLib

from gradience.backend.utils.subprocess import GradienceSubprocess


class FlatpakGSettings():
    def __init__(self):
        self.subprocess = GradienceSubprocess()

    def list_contents_async(self, callback:callable, dir_path:str):
        dconf_cmd = ["dconf", "list", dir_path]

        try:
            self.subprocess.run(callback, dconf_cmd, allow_escaping=True)
        except GLib.GError:
            raise

    def read_value_async(self, callback:callable, key_path:str):
        dconf_cmd = ["dconf", "read", key_path]

        try:
            self.subprocess.run(callback, dconf_cmd, allow_escaping=True)
        except GLib.GError:
            raise

    def write_value_async(self, callback:callable, key_path:str, value:GLib.Variant):
        dconf_cmd = ["dconf", "write", key_path, value]

        try:
            self.subprocess.run(callback, dconf_cmd, allow_escaping=True)
        except GLib.GError:
            raise

    def reset_value_async(self, callback:callable, dir_path:str = None, key_path:str = None):
        dconf_cmd = ["dconf", "reset"]

        if not dir_path and not key_path:
            raise ValueError("You need to either specify `dir_path` or `key_path` parameter")

        if dir_path:
            dconf_cmd.append(dir_path)
        elif key_path:
            dconf_cmd.append(key_path)

        try:
            self.subprocess.run(callback, dconf_cmd, allow_escaping=True)
        except GLib.GError:
            raise
