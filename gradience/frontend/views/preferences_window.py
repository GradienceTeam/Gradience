# preferences_window.py
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

from gi.repository import GLib, Gtk, Adw

from gradience.backend.flatpak_overrides import create_gtk_user_override, remove_gtk_user_override
from gradience.backend.flatpak_overrides import create_gtk_global_override, remove_gtk_global_override

from gradience.frontend.widgets.reset_preset_group import GradienceResetPresetGroup
from gradience.frontend.views.main_window import GradienceMainWindow

from gradience.backend.constants import rootdir

from gradience.backend.logger import Logger

logging = Logger()


@Gtk.Template(resource_path=f"{rootdir}/ui/preferences_window.ui")
class GradiencePreferencesWindow(Adw.PreferencesWindow):
    __gtype_name__ = "GradiencePreferencesWindow"

    general_page = Gtk.Template.Child()
    theming_page = Gtk.Template.Child()

    gtk4_user_theming_switch = Gtk.Template.Child()
    gtk4_global_theming_switch = Gtk.Template.Child()

    gtk3_user_theming_switch = Gtk.Template.Child()
    gtk3_global_theming_switch = Gtk.Template.Child()

    jsdelivr_switch = Gtk.Template.Child()

    monet_engine_switch = Gtk.Template.Child()
    gnome_shell_engine_switch = Gtk.Template.Child()

    def __init__(self, parent, **kwargs):
        super().__init__(**kwargs)

        self.parent = parent
        self.settings = parent.settings

        self.app = self.parent.get_application()
        self.win = self.app.get_active_window()

        self.set_transient_for(self.win)

        self.setup()

    def setup(self):
        self.setup_flatpak_group()
        self.setup_theme_engines_group()
        self.setup_reset_preset_group()
        self.setup_jsdelivr()

    def setup_reset_preset_group(self):
        self.reset_preset_group = GradienceResetPresetGroup(self)

        self.theming_page.add(self.reset_preset_group)

    def setup_jsdelivr(self):
        self.jsdelivr_switch.set_active(self.app.use_jsdelivr)
        self.jsdelivr_switch.connect(
            "notify::active", self.on_jsdelivr_switch_toggled
        )

    def setup_theme_engines_group(self):
        self.gnome_shell_engine_switch.set_active("shell" in self.win.enabled_theme_engines)
        self.monet_engine_switch.set_active("monet" in self.win.enabled_theme_engines)

        self.gnome_shell_engine_switch.connect(
            "notify::active", self.on_gnome_shell_engine_switch_toggled
        )

        self.monet_engine_switch.connect(
            "notify::active", self.on_monet_engine_switch_toggled
        )

    def setup_flatpak_group(self):
        user_flatpak_theming_gtk4 = self.settings.get_boolean(
            "user-flatpak-theming-gtk4"
        )

        user_flatpak_theming_gtk3 = self.settings.get_boolean(
            "user-flatpak-theming-gtk3"
        )

        self.gtk4_user_theming_switch.set_active(
            user_flatpak_theming_gtk4
        )

        # self.gtk4_global_theming_switch.set_active(global_flatpak_theming_gtk4)

        self.gtk3_user_theming_switch.set_active(
            user_flatpak_theming_gtk3
        )

        # self.gtk3_global_theming_switch.set_active(global_flatpak_theming_gtk3)

        self.gtk4_user_theming_switch.connect(
            "notify::active", self.on_gtk4_user_theming_switch_toggled
        )

        self.gtk3_user_theming_switch.connect(
            "notify::active", self.on_gtk3_user_theming_switch_toggled
        )

    def on_gtk4_user_theming_switch_toggled(self, widget, *args):
        if widget.get_active():
            create_gtk_user_override(self.settings, "gtk4", self)
        else:
            remove_gtk_user_override(self.settings, "gtk4", self)

        logging.debug(
            f"user-flatpak-theming-gtk4: {self.settings.get_boolean('user-flatpak-theming-gtk4')}"
        )

    def on_gtk3_user_theming_switch_toggled(self, widget, *args):
        if widget.get_active():
            create_gtk_user_override(self.settings, "gtk3", self)
        else:
            remove_gtk_user_override(self.settings, "gtk3", self)

        logging.debug(
            f"user-flatpak-theming-gtk3: {self.settings.get_boolean('user-flatpak-theming-gtk3')}"
        )

    def on_gtk4_global_theming_switch_toggled(self, widget, *args):
        if widget.get_active():
            create_gtk_global_override(self.settings, "gtk4", self)
        else:
            remove_gtk_global_override(self.settings, "gtk4", self)

            logging.debug(
                f"global-flatpak-theming-gtk4: {self.settings.get_boolean('global-flatpak-theming-gtk4')}"
            )

    def on_gtk3_global_theming_switch_toggled(self, widget, *args):
        if widget.get_active():
            create_gtk_global_override(self.settings, "gtk3", self)
        else:
            remove_gtk_global_override(self.settings, "gtk3", self)

            logging.debug(
                f"global-flatpak-theming-gtk3: {self.settings.get_boolean('global-flatpak-theming-gtk3')}"
            )

    def on_gnome_shell_engine_switch_toggled(self, widget, *args):
        if widget.get_active():
            self.win.enabled_theme_engines.add("shell")
        else:
            self.win.enabled_theme_engines.remove("shell")

        enabled_engines = GLib.Variant.new_strv(list(self.win.enabled_theme_engines))
        self.settings.set_value("enabled-theme-engines", enabled_engines)

        self.win.reload_theming_page()

        logging.debug(
                f"enabled-theme-engines: {self.settings.get_value('enabled-theme-engines')}"
        )

    def on_monet_engine_switch_toggled(self, widget, *args):
        if widget.get_active():
            self.win.enabled_theme_engines.add("monet")
        else:
            self.win.enabled_theme_engines.remove("monet")

        enabled_engines = GLib.Variant.new_strv(list(self.win.enabled_theme_engines))
        self.settings.set_value("enabled-theme-engines", enabled_engines)

        self.win.reload_theming_page()

        logging.debug(
                f"enabled-theme-engines: {self.settings.get_value('enabled-theme-engines')}"
        )

    def on_jsdelivr_switch_toggled(self, widget, *args):
        if widget.get_active():
            self.app.use_jsdelivr = True
        else:
            self.app.use_jsdelivr = False

        self.settings.set_boolean("use-jsdelivr", self.app.use_jsdelivr)

        logging.debug(
                f"use-jsdelivr: {self.settings.get_value('use-jsdelivr')}"
        )
