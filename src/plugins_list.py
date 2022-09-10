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


USER_PLUGIN_DIR = os.path.join(
    os.environ.get("XDG_DATA_HOME", os.environ["HOME"] + "/.local/share"),
    "gradience",
    "plugins",
)


class GradiencePluginsList:
    """Represent the plugin group in Advanced"""

    def __init__(self, win):

        self.win = win

        self.check_if_plugin_dir_exists()

        self.pm = PluginManager()

        self.pm.setPluginPlaces(
            [
                USER_PLUGIN_DIR,
            ]
        )
        self.pm.collectPlugins()
        self.rows = {}

        for pluginInfo in self.pm.getAllPlugins():
            pluginInfo.plugin_object.activate()

    @staticmethod
    def check_if_plugin_dir_exists():
        """Check if the plugin directory exists, if not, create it"""
        if not os.path.exists(USER_PLUGIN_DIR):
            os.makedirs(USER_PLUGIN_DIR)
            return False
        return True

    def to_group(self):
        group = Adw.PreferencesGroup()
        group.set_title(_("Plugins"))
        group.set_description(
            _(
                "Plugins add additional features to Gradience, plugins are made by Gradience community and can make issues."
            )
        )
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

    def apply(self):
        for pluginInfo in self.pm.getAllPlugins():
            pluginInfo.plugin_object.apply()
