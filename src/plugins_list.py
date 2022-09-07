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

from gi.repository import Adw
from yapsy.PluginManager import PluginManager
from .plugin_row import GradiencePluginRow


class GradiencePluginsList:
    def __init__(self, win):

        self.win = win

        self.pm = PluginManager()
        self.pm.setPluginPlaces(
            [
                os.path.join(
                    os.environ.get("XDG_CONFIG_HOME",
                                   os.environ["HOME"] + "/.config"),
                    "gradience_plugins",
                )
            ]
        )
        self.pm.collectPlugins()
        self.rows = {}

        for pluginInfo in self.pm.getAllPlugins():
            pluginInfo.plugin_object.activate()

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
        group.set_description(
            _("Plugins add additional features to Gradience, plugins are made by Gradience community and can make issues."))
        if self.pm:
            for pluginInfo in self.pm.getAllPlugins():
                row = GradiencePluginRow(pluginInfo.plugin_object)
                self.rows[pluginInfo.plugin_object.plugin_id] = row
                group.add(row)
        else:
            row = Adw.ActionRow()
            row.set_title(_("No plugins found"))
            group.add(row)
        return group

    def save(self):
        saved = {}
        for pluginInfo in self.pm.getAllPlugins():
            saved[pluginInfo.plugin_object.plugin_id] = pluginInfo.plugin_object.save()
        return saved

    def validate(self):
        errors = []
        for pluginInfo in self.pm.getAllPlugins():
            error, detail = pluginInfo.plugin_object.validate()
            if error:
                errors.append(detail)
        return errors
