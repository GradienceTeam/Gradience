# plugins_list.py
#
# Change the look of Adwaita, with ease
# Copyright (C) 2022  Gradience Team
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
from pathlib import Path
import importlib
import pkgutil
from .plugin_row import GradiencePluginRow
from gi.repository import Gtk, Adw, Gio, Gdk


class GradiencePluginsList:
    def __init__(self):
        self.discoverd_plugins = {
            name: importlib.import_module(name)
            for finder, name, ispkg
            in pkgutil.iter_modules()
            if name.startswith('gradience_')
        }

        self.plugins = {}

        for plugin_id, plugin in self.plugins.items():
            self.plugins[plugin_id] = plugin.GradiencePlugin()

        print(self.plugins)

    def load_all_custom_settings(self, settings):
        for plugin_id, plugin in self.plugins.items():
            plugin.load_custom_settings(settings)

    def get_all_custom_settings_for_preset(self):
        custom_settings = {}
        for plugin_id, plugin in self.plugins.items():
            custom_settings[plugin_id] = plugin.get_custom_settings_for_preset()

    def to_group(self):
        group = Adw.PreferencesGroup()
        group.set_title(_("Plugins"))
        for plugin_id, plugin in self.plugins:
            row = GradiencePluginRow(plugin.name, plugin_id)
            group.add(row)
        else:
            row = Adw.ActionRow()
            row.set_title(_("No plugins found"))
            group.add(row)
        return group

