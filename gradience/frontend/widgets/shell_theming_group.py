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

from enum import Enum

from gi.repository import Gio, Gtk, Adw

from gradience.backend.theming.shell import ShellTheme
from gradience.backend.constants import rootdir

from gradience.frontend.views.shell_prefs_window import GradienceShellPrefsWindow

from gradience.backend.logger import Logger

logging = Logger()


@Gtk.Template(resource_path=f"{rootdir}/ui/shell_theming_group.ui")
class GradienceShellThemingGroup(Adw.PreferencesGroup):
    __gtype_name__ = "GradienceShellThemingGroup"

    variant_row = Gtk.Template.Child("variant-row")
    shell_theming_expander = Gtk.Template.Child("shell-theming-expander")
    other_options_row = Gtk.Template.Child("other-options-row")

    def __init__(self, parent, **kwargs):
        super().__init__(**kwargs)

        self.parent = parent
        self.settings = parent.settings
        self.app = self.parent.get_application()

        #self.setup_signals()
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
        self.setup_variant_row()

        self.shell_theming_expander.add_row(self.other_options_row)

    def setup_variant_row(self):
        variant_store = Gtk.StringList()
        variant_store.append(_("Dark"))
        variant_store.append(_("Light"))

        self.variant_row.set_model(variant_store)

    # TODO: Maybe allow it when using export option?
    '''def setup_version_row(self):
        version_store = Gtk.StringList()
        version_store.append(_("Auto"))
        version_store.append(_("43"))
        version_store.append(_("42"))

        self.shell_version_row.set_model(version_store)'''

    def on_toggle_state_change(self, *_args):
        shell_theming_enabled = self.settings.get_boolean("shell-theming-enabled")
        logging.debug(f"shell-theming-enabled key state: {shell_theming_enabled}")

    @Gtk.Template.Callback()
    def on_custom_colors_button_clicked(self, *_args):
        self.shell_pref_window = GradienceShellPrefsWindow(self.parent)
        self.shell_pref_window.present()

    @Gtk.Template.Callback()
    def on_apply_button_clicked(self, *_args):
        variant_pos = self.variant_row.props.selected

        class variantEnum(Enum):
            DARK = 0
            LIGHT = 1

        def __get_variant_string():
            if variant_pos == variantEnum.DARK.value:
                return "dark"
            elif variant_pos == variantEnum.LIGHT.value:
                return "light"

        variant_str = __get_variant_string()

        try:
            ShellTheme().apply_theme(self.app.preset, variant_str)
        except (ValueError, OSError, GLib.GError) as e:
            logging.error("An error occurred while generating a Shell theme.", exc=e)
        else:
            logging.debug("It works! \o/")

    @Gtk.Template.Callback()
    def on_remove_button_clicked(self, *_args):
        # TODO: Make this function actually remove Shell theme
        ShellTheme().unset_shell_theme()

    @Gtk.Template.Callback()
    def on_restore_button_clicked(self, *_args):
        logging.debug("Nothing here yet /o\ ")
