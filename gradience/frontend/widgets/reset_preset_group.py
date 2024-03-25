# reset_preset_group.py
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

from gi.repository import GLib, Gtk, Adw

from gradience.backend.constants import rootdir
from gradience.backend.logger import Logger
from gradience.backend.theming.preset import PresetUtils

logging = Logger()


@Gtk.Template(resource_path=f"{rootdir}/ui/reset_preset_group.ui")
class GradienceResetPresetGroup(Adw.PreferencesGroup):
    __gtype_name__ = "GradienceResetPresetGroup"

    def __init__(self, parent, **kwargs):
        super().__init__(**kwargs)

        self.parent = parent

        self.app = self.parent.get_application()
        self.win = self.parent

        self.setup_signals()
        self.setup()

    def setup_signals(self):
        pass

    def setup(self):
        pass

    @Gtk.Template.Callback()
    def on_libadw_restore_button_clicked(self, *_args):
        try:
            PresetUtils().restore_preset("gtk4")
        except GLib.GError:
            self.parent.add_toast(
                Adw.Toast(title=_("Unable to restore GTK 4 backup"))
            )
        else:
            toast = Adw.Toast(
                title=_("GTK 4 preset has been restored. Log out to apply changes."),
            )
            self.parent.add_toast(toast)

    @Gtk.Template.Callback()
    def on_libadw_reset_button_clicked(self, *_args):
        try:
            PresetUtils().reset_preset("gtk4")
        except GLib.GError:
            self.parent.add_toast(
                Adw.Toast(title=_("Unable to delete current preset"))
            )
        else:
            toast = Adw.Toast(
                title=_("GTK 4 theme has been reset. Log out to apply changes."),
            )
            self.parent.add_toast(toast)


    @Gtk.Template.Callback()
    def on_gtk3_restore_button_clicked(self, *_args):
        try:
            PresetUtils().restore_preset("gtk3")
        except GLib.GError:
            self.parent.add_toast(
                Adw.Toast(title=_("Unable to restore GTK 3 backup"))
            )
        else:
            toast = Adw.Toast(
                title=_("GTK 3 preset has been restored. Log out to apply changes."),
            )
            self.parent.add_toast(toast)

    @Gtk.Template.Callback()
    def on_gtk3_reset_button_clicked(self, *_args):
        try:
            PresetUtils().reset_preset("gtk3")
        except GLib.GError:
            self.parent.add_toast(
                Adw.Toast(title=_("Unable to delete current preset"))
            )
        else:
            toast = Adw.Toast(
                title=_("GTK 3 theme has been reset. Log out to apply changes."),
            )
            self.parent.add_toast(toast)
