# plugins_list.py
#
# Change the look of Adwaita, with ease
# Copyright (C) 2022  Adwaita Manager Team
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

from .plugins.gtk4 import AdwcustomizerGtk4Plugin
import os
from pathlib import Path
import importlib
class AdwcustomizerPluginsList:
    def __init__(self):
        self.plugins = { # AdwCustomizerTeam plugins
            "gtk4": AdwcustomizerGtk4Plugin()
        }
        self.add_user_plugins()

    def add_user_plugins(self):
        self.user_plugin_dir = Path(os.environ.get("XDG_DATA_HOME", os.environ["HOME"])) / ".local" / "share" / "AdwCustomizer" / "plugins"
        if self.user_plugin_dir.exists():
            for path, _, name in os.walk(self.user_plugin_dir):
                print(name[0])
        else:
            print("No plugins dir found")


    def load_all_custom_settings(self, settings):
        for plugin_id, plugin in self.plugins.items():
            plugin.load_custom_settings(settings[plugin_id])

    def get_all_custom_settings_for_preset(self):
        custom_settings = {}
        for plugin_id, plugin in self.plugins.items():
            custom_settings[plugin_id] = plugin.get_custom_settings_for_preset()