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

from gi.repository import GObject, GLib, Gio, Gtk, Adw

from gradience.backend.utils.gnome import is_gnome_available
from gradience.backend.constants import rootdir
from gradience.backend.exceptions import UnsupportedShellVersion
from gradience.backend.logger import Logger

from gradience.backend.theming.shell import ShellTheme

from gradience.frontend.schemas.shell_schema import shell_schema
from gradience.frontend.dialogs.unsupported_shell_version_dialog import GradienceUnsupportedShellVersionDialog
from gradience.frontend.views.shell_prefs_window import GradienceShellPrefsWindow

logging = Logger()


@Gtk.Template(resource_path=f"{rootdir}/ui/shell_theming_group.ui")
class GradienceShellThemingGroup(Adw.PreferencesGroup):
    __gtype_name__ = "GradienceShellThemingGroup"

    variant_row = Gtk.Template.Child("variant-row")
    shell_theming_expander = Gtk.Template.Child("shell-theming-expander")
    other_options_row = Gtk.Template.Child("other-options-row")

    def __init__(self, parent, **kwargs):
        super().__init__(**kwargs)

        self.shell_colors = {}

        self.parent = parent
        self.settings = parent.settings

        self.app = parent.get_application()
        self.win = self.app.get_active_window()
        self.toast_overlay = parent.toast_overlay

        self.setup_signals()
        self.setup()

    def setup_signals(self):
        self.app.connect("preset-reload", self.reload_colors)

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

    def reload_colors(self, *args):
        try:
            for variable in shell_schema["variables"]:
                self.set_colors(variable)
        except Exception as e:
            logging.error("An unexpected error occurred while loading variable colors.", exc=e)
            self.toast_overlay.add_toast(
                Adw.Toast(
                    title=_("An unexpected error occurred while loading variable colors."))
            )

    def set_colors(self, variable):
        try:
            self.shell_colors[variable["name"]] = variable["default_value"]
        except KeyError:
            try:
                self.shell_colors[variable["name"]] = self.app.variables[variable["var_name"]]
            except KeyError:
                raise

    @Gtk.Template.Callback()
    def on_custom_colors_button_clicked(self, *_args):
        self.shell_pref_window = GradienceShellPrefsWindow(self.parent, self.shell_colors)
        self.shell_pref_window.present()

    @Gtk.Template.Callback()
    def on_apply_button_clicked(self, *_args):
        if not is_gnome_available():
            dialog = Adw.MessageDialog(transient_for=self.win, heading=_("GNOME Shell Missing"),
                body=_("This Theme Engine is designed to work only on systems running GNOME. You can still generate themes on other desktop environments, but it won't have any affect on them."))

            dialog.add_response("disable-engine", _("Disable Engine"))
            dialog.add_response("ok", _("Okay"))
            dialog.set_response_appearance("disable-engine", Adw.ResponseAppearance.DESTRUCTIVE)
            dialog.set_default_response("ok")

            dialog.connect("response", self.on_shell_missing_response)
            dialog.present()
        else:
            self.apply_shell_theme()

    def apply_shell_theme(self):
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
            ShellTheme().apply_theme_async(self, self._on_shell_theme_done,
                                            variant_str, self.app.preset)
        except UnsupportedShellVersion:
            logging.error("Unsupported GNOME Shell version detected.")
            GradienceUnsupportedShellVersionDialog(self.parent).present()
        except (ValueError, OSError, GLib.GError) as e:
            logging.error(
                "An error occurred while generating a Shell theme.", exc=e)
            self.toast_overlay.add_toast(
                Adw.Toast(
                    title=_("An error occurred while generating a Shell theme."))
            )

    def _on_shell_theme_done(self, source_widget:GObject.Object, result:Gio.AsyncResult,
                                user_data:GObject.GPointer):
        logging.debug("It works! \o/")
        self.toast_overlay.add_toast(
            Adw.Toast(title=_("Shell theme applied successfully."))
        )

    def on_shell_missing_response(self, widget, response, *args):
        if response == "disable-engine":
            self.win.enabled_theme_engines.remove("shell")

            enabled_engines = GLib.Variant.new_strv(list(self.win.enabled_theme_engines))
            self.settings.set_value("enabled-theme-engines", enabled_engines)

            self.win.reload_theming_page()
        elif response == "ok":
            self.apply_shell_theme()

    @Gtk.Template.Callback()
    def on_remove_button_clicked(self, *_args):
        # TODO: Make this function actually remove Shell theme
        ShellTheme().reset_shell_theme()

    @Gtk.Template.Callback()
    def on_restore_button_clicked(self, *_args):
        logging.debug("Nothing here yet /o\ ")
