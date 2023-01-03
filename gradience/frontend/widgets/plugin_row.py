# plugin_row.py
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

from gi.repository import Gtk, Adw

from gradience.frontend.views.no_plugin_window import GradienceNoPluginPrefWindow
from gradience.backend.globals import user_plugin_dir
from gradience.backend.constants import rootdir

from gradience.backend.logger import Logger

logging = Logger()


@Gtk.Template(resource_path=f"{rootdir}/ui/plugin_row.ui")
class GradiencePluginRow(Adw.ActionRow):
    __gtype_name__ = "GradiencePluginRow"

    switch = Gtk.Template.Child("switch")
    settings_button = Gtk.Template.Child("settings-button")
    remove_button = Gtk.Template.Child("remove-button")

    def __init__(self, plugin_object, preset, plugins_list, **kwargs):
        super().__init__(**kwargs)

        self.plugins_list = plugins_list

        self.plugin_object = plugin_object
        if not os.path.exists(
            os.path.join(
                user_plugin_dir,
                f"{self.plugin_object.plugin_id}.yapsy-plugin"
            )
        ):
            self.remove_button.set_visible(False)

        self.set_name(plugin_object.plugin_id)
        self.set_title(plugin_object.title)
        self.set_subtitle("@" + plugin_object.plugin_id)

        self.enabled_plugins = self.plugins_list.enabled_plugins
        if self.plugin_object.plugin_id in self.enabled_plugins:
            self.switch.set_active(True)

        self.give_preset_settings(preset)

    @Gtk.Template.Callback()
    def on_settings_plugin_clicked(self, *_args):
        has_setting = self.plugin_object.open_settings()
        if not has_setting:
            win = GradienceNoPluginPrefWindow()
            win.set_transient_for(self.plugins_list.win)
            win.present()

    @Gtk.Template.Callback()
    def on_remove_plugin_clicked(self, *_args):
        plugin_yapsy_file = (
            os.path.join(
                user_plugin_dir,
                f"{self.plugin_object.plugin_id}.yapsy-plugin"
            )
        )
        logging.debug(f"remove {plugin_yapsy_file}")
        try:
            os.remove(plugin_yapsy_file)
        except FileNotFoundError:
            error_dialog = Adw.MessageDialog(
                heading=_("Unable to remove"),
                body=_("This is a system plugin, and cannot be removed."),
            )
            error_dialog.add_response("close", _("Close"))
            error_dialog.present()
        logging.debug(f"remove {plugin_yapsy_file}")
        Gtk.Application.get_default().reload_plugins()

    @Gtk.Template.Callback()
    def on_switch_toggled(self, *_args):
        if self.switch.get_active():
            self.plugins_list.enable_plugin(self.plugin_object.plugin_id)
        else:
            self.plugins_list.disable_plugin(self.plugin_object.plugin_id)

    def give_preset_settings(self, preset_settings):
        self.preset_settings = preset_settings
        self.plugin_object.give_preset_settings(preset_settings)
