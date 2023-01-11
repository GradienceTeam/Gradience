# shell_theming_group.py
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

from gi.repository import Gio, Gtk, Adw

from gradience.backend.constants import rootdir

from gradience.frontend.views.shell_prefs_window import GradienceShellPrefsWindow

from gradience.backend.logger import Logger

logging = Logger()


@Gtk.Template(resource_path=f"{rootdir}/ui/shell_theming_group.ui")
class GradienceShellThemingGroup(Adw.PreferencesGroup):
    __gtype_name__ = "GradienceShellThemingGroup"

    shell_theming_expander = Gtk.Template.Child("shell-theming-expander")
    shell_pref_button = Gtk.Template.Child("shell-pref-button")

    def __init__(self, parent, **kwargs):
        super().__init__(**kwargs)

        self.parent = parent
        self.settings = parent.settings
        self.app = self.parent.get_application()

        self.setup_signals()
        self.setup()

    def setup_signals(self):
        self.settings.bind(
            "shell-theming-enabled",
            self.shell_theming_expander,
            "enable-expansion",
            Gio.SettingsBindFlags.DEFAULT
        )

        self.settings.connect("changed::shell-theming-enabled",
            self.on_toggle_state_change
        )

    def setup(self):
        pass

    def on_toggle_state_change(self, *_args):
        shell_theming_enabled = self.settings.get_boolean("shell-theming-enabled")
        logging.debug("It works! \o/")
        logging.debug(f"shell-theming-enabled key state: {shell_theming_enabled}")

    @Gtk.Template.Callback()
    def on_shell_pref_button_clicked(self, *_args):
        self.shell_pref_window = GradienceShellPrefsWindow(self.parent)
        self.shell_pref_window.present()
