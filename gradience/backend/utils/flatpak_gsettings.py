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
        pass

    def list_keys_async(self, callback:callable, schema_id:str):
        dconf_cmd = ["gsettings", "list-keys", schema_id]

        try:
            GradienceSubprocess().run(callback, dconf_cmd, allow_escaping=True)
        except GLib.GError:
            raise

    def read_value_async(self, callback:callable, schema_id:str, key:str):
        dconf_cmd = ["gsettings", "get", schema_id, key]

        try:
            GradienceSubprocess().run(callback, dconf_cmd, allow_escaping=True)
        except GLib.GError:
            raise

    def write_value_async(self, callback:callable, schema_id:str, key:str, value:str):
        dconf_cmd = ["gsettings", "set", schema_id, key, value]

        try:
            GradienceSubprocess().run(callback, dconf_cmd, allow_escaping=True)
        except GLib.GError:
            raise

    def reset_value_async(self, callback:callable, schema_id:str, key:str = None):
        dconf_cmd = ["gsettings", "reset", schema_id, key]

        try:
            GradienceSubprocess().run(callback, dconf_cmd, allow_escaping=True)
        except GLib.GError:
            raise
