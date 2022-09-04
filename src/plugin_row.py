# plugin_row.py
#
# Change the look of Adwaita, with ease
# Copyright (C) 2022 Gradience Team
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

from gi.repository import Gtk, Gdk, Adw

from .modules.utils import buglog
from .constants import rootdir
import os


@Gtk.Template(resource_path=f"{rootdir}/ui/plugin_row.ui")
class GradiencePluginRow(Adw.ActionRow):
    __gtype_name__ = "GradiencePluginRow"

    def __init__(self, plugin_object, **kwargs):
        super().__init__(**kwargs)

        self.plugin_object = plugin_object
        self.set_name(plugin_object.plugin_id)
        self.set_title(plugin_object.title)
        self.set_subtitle("@" + plugin_object.plugin_id)

        switch = Gtk.Template.Child("switch")
        settings_button = Gtk.Template.Child("settings-button")
        remove_button = Gtk.Template.Child("remove-button")

    @Gtk.Template.Callback()
    def on_settings_plugin_clicked(self, *_args):
        self.plugin_object.open_settings()

    @Gtk.Template.Callback()
    def on_remove_plugin_clicked(self, *_args):
        # try:
        #     os.remove(os.path.join(
        #         os.environ.get("XDG_CONFIG_HOME",
        #                         os.environ["HOME"] + "/.config"),
        #         "gradience_plugins",
        #         self.plugin_object.plugin_id + "."
        #     ))
        # except Exception as exception:
        #     print(exception.with_traceback())
        #     self.toast_overlay.add_toast(
        #         Adw.Toast(title=_("Unable to delete preset"))
        #     )
        # else:
        #     self.toast_overlay.add_toast(
        #         Adw.Toast(title=_("Preset removed"))
        #     )
        # finally:
        #     self.win.reload_pref_group()
        print("delete")

    @Gtk.Template.Callback()
    def on_switch_toggled(self, *_args):
        buglog("toggled")

        Gtk.Application.get_default().reload_plugins()
