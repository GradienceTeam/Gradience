# preferences_window.py
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

from gi.repository import Gtk, Adw

from gradience.constants import rootdir
from gradience.utils.flatpak_overrides import (
    create_gtk_user_override,
    remove_gtk_user_override,
)
from gradience.utils.flatpak_overrides import (
    create_gtk_global_override,
    remove_gtk_global_override,
)
from gradience.utils.utils import buglog


@Gtk.Template(resource_path=f"{rootdir}/ui/preferences_window.ui")
class GradiencePreferencesWindow(Adw.PreferencesWindow):
    __gtype_name__ = "GradiencePreferencesWindow"

    allow_gtk4_flatpak_theming_user = Gtk.Template.Child()
    allow_gtk4_flatpak_theming_global = Gtk.Template.Child()

    allow_gtk3_flatpak_theming_user = Gtk.Template.Child()
    allow_gtk3_flatpak_theming_global = Gtk.Template.Child()

    def __init__(self, parent, **kwargs):
        super().__init__(**kwargs)

        self.parent = parent
        self.settings = parent.settings

        self.setup()

    def setup(self):

        self.setup_flatpak_group()

    def setup_flatpak_group(self):
        user_flatpak_theming_gtk4 = self.settings.get_boolean(
            "user-flatpak-theming-gtk4"
        )

        user_flatpak_theming_gtk3 = self.settings.get_boolean(
            "user-flatpak-theming-gtk3"
        )

        self.allow_gtk4_flatpak_theming_user.set_state(
            user_flatpak_theming_gtk4)
        # self.allow_gtk4_flatpak_theming_global.set_state(global_flatpak_theming_gtk4)

        self.allow_gtk3_flatpak_theming_user.set_state(
            user_flatpak_theming_gtk3)
        # self.allow_gtk3_flatpak_theming_global.set_state(global_flatpak_theming_gtk3)

        self.allow_gtk4_flatpak_theming_user.connect(
            "state-set", self.on_allow_gtk4_flatpak_theming_user_toggled
        )

        self.allow_gtk3_flatpak_theming_user.connect(
            "state-set", self.on_allow_gtk3_flatpak_theming_user_toggled
        )

    def on_allow_gtk4_flatpak_theming_user_toggled(self, *args):
        state = self.allow_gtk4_flatpak_theming_user.props.state

        if not state:
            create_gtk_user_override(self, self.settings, "gtk4")
        else:
            remove_gtk_user_override(self, self.settings, "gtk4")

            buglog(
                f"user-flatpak-theming-gtk4: {self.settings.get_boolean('user-flatpak-theming-gtk4')}"
            )

    def on_allow_gtk3_flatpak_theming_user_toggled(self, *args):
        state = self.allow_gtk3_flatpak_theming_user.props.state

        if not state:
            create_gtk_user_override(self, self.settings, "gtk3")
        else:
            remove_gtk_user_override(self, self.settings, "gtk3")

            buglog(
                f"user-flatpak-theming-gtk3: {self.settings.get_boolean('user-flatpak-theming-gtk3')}"
            )

    def on_allow_gtk4_flatpak_theming_global_toggled(self, *args):
        state = self.allow_gtk4_flatpak_theming_global.props.state

        if not state:
            create_gtk_global_override(self, self.settings, "gtk4")
        else:
            remove_gtk_global_override(self, self.settings, "gtk4")

            buglog(
                f"global-flatpak-theming-gtk4: {self.settings.get_boolean('global-flatpak-theming-gtk4')}"
            )

    def on_allow_gtk3_flatpak_theming_global_toggled(self, *args):
        state = self.allow_gtk3_flatpak_theming_global.props.state

        if not state:
            create_gtk_global_override(self, self.settings, "gtk3")
        else:
            remove_gtk_global_override(self, self.settings, "gtk3")

            buglog(
                f"global-flatpak-theming-gtk3: {self.settings.get_boolean('global-flatpak-theming-gtk3')}"
            )
