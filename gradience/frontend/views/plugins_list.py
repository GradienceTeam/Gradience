# plugins_list.py
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

from gi.repository import Adw, GLib
from yapsy.PluginManager import PluginManager

from gradience.frontend.widgets.plugin_row import GradiencePluginRow
from gradience.backend.globals import user_plugin_dir, system_plugin_dir

from gradience.backend.logger import Logger

logging = Logger()


class GradiencePluginsList:
    """Represent the plugin group in Advanced"""

    def __init__(self, win):

        self.win = win

        self.check_if_plugin_dir_exists()

        self.app = self.win.get_application()
        self.enabled_plugins = set(
            self.app.settings.get_value("enabled-plugins").unpack()
        )
        self.rows = {}

        self.reload()

    def reload(self):
        self.pm = PluginManager()
        self.pm.setPluginPlaces([user_plugin_dir, system_plugin_dir])
        self.pm.collectPlugins()
        for pluginInfo in self.pm.getAllPlugins():
            pluginInfo.plugin_object.activate()

        self.app = self.win.get_application()
        self.enabled_plugins = set(
            self.app.settings.get_value("enabled-plugins").unpack()
        )

    def save_enabled_plugins(self):
        self.app.settings.set_value(
            "enabled-plugins", GLib.Variant("as", list(self.enabled_plugins))
        )

    def enable_plugin(self, plugin_id):
        self.enabled_plugins.add(plugin_id)
        self.save_enabled_plugins()

    def disable_plugin(self, plugin_id):
        self.enabled_plugins.remove(plugin_id)
        self.save_enabled_plugins()

    @staticmethod
    def check_if_plugin_dir_exists():
        """Check if the plugin directory exists, if not, create it"""
        if not os.path.exists(user_plugin_dir):
            os.makedirs(user_plugin_dir)
            return False
        return True

    def to_group(self):
        preset = {
            "variables": self.app.variables,
            "palette": self.app.palette,
            "custom_css": self.app.custom_css,
        }
        group = Adw.PreferencesGroup()
        group.set_title(_("Plugins"))
        group.set_description(
            _(
                "Plugins add additional features to Gradience, plugins are "
                "made by Gradience community and can cause issues."
            )
        )
        empty = True
        for pluginInfo in self.pm.getAllPlugins():
            row = GradiencePluginRow(pluginInfo.plugin_object, preset, self)
            self.rows[pluginInfo.plugin_object.plugin_id] = row
            group.add(row)
            empty = False
        if empty:
            row = Adw.ActionRow()
            row.set_title(_("No Plugins Found."))
            group.add(row)
        return group

    def save(self):
        saved = {}
        for pluginInfo in self.pm.getAllPlugins():
            try:
                saved[pluginInfo.plugin_object.plugin_id] = pluginInfo.plugin_object.save()
            except AttributeError:
                logging.error(f"{pluginInfo.plugin_object.plugin_id} doesn't have 'apply'")
        return saved

    def validate(self):
        errors = []
        for pluginInfo in self.pm.getAllPlugins():
            try:
                error, detail = pluginInfo.plugin_object.validate()
                if error:
                    errors.append(detail)
            except AttributeError:
                logging.error(f"Plugin {pluginInfo.plugin_object.plugin_id} doesn't have 'validatee'")
        return errors

    def apply(self):
        for pluginInfo in self.pm.getAllPlugins():
            if pluginInfo.plugin_object.plugin_id in self.enabled_plugins:
                logging.debug(pluginInfo.plugin_object)
                try:
                    pluginInfo.plugin_object.apply()
                except AttributeError:
                    logging.error(f"Plugin {pluginInfo.plugin_object.plugin_id} doesn't have 'apply'")
