# main.py
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
import sys
import threading

from pathlib import Path
from material_color_utilities_python import hexFromArgb
from gi.repository import GObject, Gtk, Gdk, Gio, Adw, GLib

from gradience.backend.globals import presets_dir, get_gtk_theme_dir
from gradience.backend.css_parser import parse_css
from gradience.backend.models.preset import Preset
from gradience.backend.theming.preset import PresetUtils
from gradience.backend.theming.monet import Monet
from gradience.backend.utils.common import to_slug_case
from gradience.backend.utils.theming import generate_gtk_css
from gradience.backend.constants import rootdir, app_id, rel_ver

from gradience.frontend.views.main_window import GradienceMainWindow
from gradience.frontend.views.plugins_list import GradiencePluginsList
from gradience.frontend.views.about_window import GradienceAboutWindow
from gradience.frontend.views.welcome_window import GradienceWelcomeWindow
from gradience.frontend.views.presets_manager_window import GradiencePresetWindow
from gradience.frontend.views.preferences_window import GradiencePreferencesWindow

from gradience.frontend.dialogs.app_type_dialog import GradienceAppTypeDialog
from gradience.frontend.dialogs.save_dialog import GradienceSaveDialog
from gradience.frontend.widgets.custom_css_group import GradienceCustomCSSGroup

from gradience.frontend.utils.actions import ActionHelpers
from gradience.frontend.schemas.preset_schema import preset_schema

from gradience.backend.logger import Logger

logging = Logger()


class GradienceApplication(Adw.Application):
    """The main application singleton class."""

    __gtype_name__ = "GradienceApplication"

    settings = Gio.Settings.new(app_id)

    def __init__(self):
        super().__init__(
            application_id=app_id,
            flags=Gio.ApplicationFlags.FLAGS_NONE
        )

        self.set_resource_base_path(rootdir)

        self.preset: Preset = None
        self.preset_name = ""

        self.variables = {}
        self.pref_variables = {}

        self.palette = {}
        self.pref_palette_shades = {}

        self.custom_css = {}
        self.custom_css_group = None

        self.custom_presets = {}
        self.global_errors = []
        self.current_css_provider = None

        self.is_dirty = False
        self.is_ready = False

        self.first_run = self.settings.get_boolean("first-run")

        self.last_opened_version = self.settings.get_string(
            "last-opened-version"
        )
        self.favourite = set(self.settings.get_value("favourite"))

        self.style_manager = Adw.StyleManager.get_default()

        self.use_jsdelivr = self.settings.get_boolean("use-jsdelivr")

    def do_activate(self):
        """Called when the application is activated."""

        self.win = self.props.active_window

        self.setup_signals()

        if not self.win:
            self.win = GradienceMainWindow(
                application=self,
                default_height=self.settings.get_int("window-height"),
                default_width=self.settings.get_int("window-width"),
                fullscreened=self.settings.get_boolean("window-fullscreen"),
                maximized=self.settings.get_boolean("window-maximized")
            )

        self.plugins_list = GradiencePluginsList(self.win)
        self.setup_plugins()

        self.actions = ActionHelpers(self)

        self.actions.create_stateful_action(
            "load_preset",
            GLib.VariantType.new("s"),
            GLib.Variant("s", "adwaita"),
            self.load_preset_action
        )

        self.actions.create_action("open_preset_directory",
                        self.open_preset_directory)

        self.actions.create_action("apply_color_scheme",
                        self.show_apply_color_scheme_dialog, ["<primary>Return"])

        self.actions.create_action("manage_presets",
                        self.show_presets_manager, ["<primary>m"])

        self.actions.create_action("preferences",
                        self.show_preferences, ["<primary>comma"])

        self.actions.create_action("save_preset",
                        self.show_save_preset_dialog, ["<primary>s"])

        self.actions.create_action("quit",
                        self.win.on_close_request, ["<primary>q"])

        self.actions.create_action("switch_to_colors_page", 
                        self.win.switch_to_colors_page, ["<alt>1"])

        self.actions.create_action("switch_to_theming_page", 
                        self.win.switch_to_theming_page, ["<alt>2"])

        self.actions.create_action("switch_to_advanced_page", 
                        self.win.switch_to_advanced_page, ["<alt>3"])

        self.actions.create_action("about",
                        self.show_about_window)

        self.load_preset_from_css()
        self.reload_user_defined_presets()

        if self.first_run:
            welcome = GradienceWelcomeWindow(self.win)
            welcome.present()
        else:
            if rel_ver != self.last_opened_version:
                welcome = GradienceWelcomeWindow(self.win, update=True)
                welcome.present()
            else:
                logging.debug("normal run")
                self.win.present()

    def setup_signals(self):
        # Custom signals
        GObject.signal_new(
            "preset-reload",
            self,
            GObject.SignalFlags.RUN_LAST,
            bool,
            (object,)
        )

    def save_favourite(self):
        self.settings.set_value(
            "favourite", GLib.Variant("as", self.favourite))

    def reload_user_defined_presets(self):
        if self.props.active_window.presets_menu.get_n_items() > 1:
            self.props.active_window.presets_menu.remove(1)

        if not os.path.exists(presets_dir):
            os.makedirs(presets_dir)

        self.custom_presets = {"user": {}}

        for repo in Path(presets_dir).iterdir():
            logging.debug(f"presets_dir.iterdir: {repo}")

            try:
                presets_list = PresetUtils().get_presets_list(repo)
            except (OSError, KeyError, AttributeError):
                logging.error("Failed to retrieve a list of presets.")
                self.toast_overlay.add_toast(
                    Adw.Toast(title=_("Failed to load list of presets"))
                )
            else:
                self.custom_presets[repo.name] = presets_list

        custom_menu_section = Gio.Menu()

        try:
            is_custom_presets = (
                self.custom_presets["user"]
                or self.custom_presets["curated"]
                or self.custom_presets["official"]
            )

            if (is_custom_presets):
                for repo, content in self.custom_presets.items():
                    for preset, preset_name in content.items():
                        logging.debug(preset_name)

                        if preset_name in self.favourite:
                            menu_item = Gio.MenuItem()
                            menu_item.set_label(preset_name)

                            if not preset.startswith("error"):
                                menu_item.set_action_and_target_value(
                                    "app.load_preset",
                                    GLib.Variant("s", "custom-" + preset))
                            else:
                                menu_item.set_action_and_target_value("")

                            custom_menu_section.append_item(menu_item)
            else:
                menu_item = Gio.MenuItem()
                menu_item.set_label(_("No presets found"))
                custom_menu_section.append_item(menu_item)

        except KeyError:
            if not os.path.exists(os.path.join(presets_dir, "user")):
                os.makedirs(os.path.join(presets_dir, "user"))

            if not os.path.exists(os.path.join(presets_dir, "curated")):
                os.makedirs(os.path.join(presets_dir, "curated"))

            if not os.path.exists(os.path.join(presets_dir, "official")):
                os.makedirs(os.path.join(presets_dir, "official"))

        open_in_file_manager_item = Gio.MenuItem()
        open_in_file_manager_item.set_label(_("Open in File Manager"))

        open_in_file_manager_item.set_action_and_target_value(
            "app.open_preset_directory"
        )

        # custom_menu_section.append_item(open_in_file_manager_item)

        self.props.active_window.presets_menu.append_section(
            _("Favorite Presets"), custom_menu_section
        )

    def show_presets_manager(self, *_args):
        presets = GradiencePresetWindow(self.win)
        presets.present()

        add_rows_thread = threading.Thread(target=presets.add_explore_rows)
        add_rows_thread.start()

    def load_preset_from_css(self):
        try:
            variables, palette, custom_css = parse_css(
                os.path.join(
                    get_gtk_theme_dir("gtk4"),
                    "gtk.css"
                )
            )

            logging.debug(f"Loaded custom CSS variables: {variables}")

            preset = {
                "name": "Preset Name",
                "variables": variables,
                "palette": palette,
                "custom_css": {
                    "gtk4": custom_css,
                    "gtk3": ""
                }
            }

            self.preset = Preset().new_from_dict(preset)
            self.load_preset_variables_from_preset()
        except OSError:  # fallback to adwaita
            logging.warning("Custom preset not found. Fallback to Adwaita")
            if self.style_manager.get_dark():
                self.load_preset_from_resource(
                    f"{rootdir}/presets/adwaita-dark.json")
            else:
                self.load_preset_from_resource(
                    f"{rootdir}/presets/adwaita.json")

    def open_preset_directory(self, *_args):
        Gtk.show_uri(
            self.win,
            f"file://{presets_dir}",
            Gdk.CURRENT_TIME
        )

    def load_preset_from_file(self, preset_path):
        logging.debug(f"load preset from file {preset_path}")

        self.preset = Preset().new_from_path(preset_path)
        self.load_preset_variables_from_preset()

    def load_preset_from_resource(self, preset_path):
        preset_text = Gio.resources_lookup_data(
            preset_path, 0).get_data().decode()

        self.preset = Preset().new_from_resource(text=preset_text)
        self.load_preset_variables_from_preset()

    def load_preset_variables_from_preset(self, preset=None):
        if preset is not None:
            self.preset = preset

        self.is_ready = False

        logging.debug(self.preset)

        self.preset_name = self.preset.display_name
        self.variables = self.preset.variables
        self.palette = self.preset.palette
        self.custom_css = self.preset.custom_css

        for key in self.variables.keys():
            if key in self.pref_variables:
                self.pref_variables[key].update_value(self.variables[key])

        for key in self.palette.keys():
            if key in self.pref_palette_shades:
                self.pref_palette_shades[key].update_shades(self.palette[key])

        self.custom_css_group.load_custom_css(self.custom_css)
        self.clear_dirty()

        self.reload_variables()

    def load_preset_variables(self, preset):
        self.is_ready = False

        self.preset_name = preset["name"]
        self.variables = preset["variables"]
        self.palette = preset["palette"]

        if "custom_css" in preset:
            self.custom_css = preset["custom_css"]
        else:
            for app_type in preset_schema["custom_css_app_types"]:
                self.custom_css[app_type] = ""

        for key in self.variables.keys():
            if key in self.pref_variables:
                self.pref_variables[key].update_value(self.variables[key])

        for key in self.palette.keys():
            if key in self.pref_palette_shades:
                self.pref_palette_shades[key].update_shades(self.palette[key])

        self.custom_css_group.load_custom_css(self.custom_css)
        self.clear_dirty()

        self.reload_variables()

    def update_theme_from_monet(self, monet, preset_variant: str, tone=20):
        palettes = monet["palettes"]

        preset_variant = preset_variant.lower()  # dark / light

        palette = {}

        for i, color in zip(range(1, 7), palettes.values()):
            palette[str(i)] = hexFromArgb(color.tone(int(tone)))
        self.pref_palette_shades["monet"].update_shades(palette)

        if preset_variant == "auto":
            if self.style_manager.get_dark():
                preset_variant = "dark"
            else:
                preset_variant = "light"

        try:
            preset_object = Monet().new_preset_from_monet(monet_palette=monet,
                                props=[tone, preset_variant], obj_only=True)
        except (OSError, AttributeError) as e:
            logging.error("An error occurred while generating preset from Monet palette.", exc=e)
            raise

        variable = preset_object.variables

        for key in variable:
            if key in self.pref_variables:
                self.pref_variables[key].update_value(variable[key])

        # TODO: Create a whole function deticated to clearing preset and custom CSS
        self.preset_name = "Preset Name"

        self.reload_variables()

    def mark_as_dirty(self):
        self.is_dirty = True

        self.props.active_window.save_preset_button.add_css_class("warning")
        self.props.active_window.save_preset_button.set_tooltip_text(_("Unsaved Changes"))

    def clear_dirty(self):
        self.is_dirty = False

        self.props.active_window.save_preset_button.get_child().set_icon_name(
            "document-save-symbolic"
        )
        self.props.active_window.save_preset_button.remove_css_class("warning")
        self.props.active_window.save_preset_button.get_child().set_label(_("Save"))
        self.props.active_window.save_preset_button.set_tooltip_text(_("Save Preset"))

    def reload_variables(self):
        parsing_errors = []
        gtk_css = generate_gtk_css("gtk4", self.preset)
        css_provider = Gtk.CssProvider()

        def on_error(_, section, error):
            start_location = section.get_start_location().chars
            end_location = section.get_end_location().chars
            line_number = section.get_end_location().lines

            parsing_errors.append(
                {
                    "error": error.message,
                    "element": gtk_css[start_location:end_location].strip(),
                    "line": gtk_css.splitlines()[line_number]
                    if line_number < len(gtk_css.splitlines())
                    else "<last line>"
                }
            )

        css_provider.connect("parsing-error", on_error)

        # In GTK 4.8, bytes are expected, in GTK 4.10, you can provider a string, with a length.
        # This patch still allows bytes for backwards compatibility, and add support for
        # strings in GTK 4.8 and before.
        # https://gitlab.gnome.org/GNOME/pygobject/-/merge_requests/231
        # Credits to https://gitlab.gnome.org/amolenaar for the patch
        if (Gtk.get_major_version(), Gtk.get_minor_version()) >= (4, 9):
            css_provider.load_from_data(gtk_css, -1)
        else:
            css_provider.load_from_data(gtk_css.encode())

        self.props.active_window.update_errors(
            self.global_errors + parsing_errors)

        # loading with the priority above user to override the applied config
        if self.current_css_provider is not None:
            Gtk.StyleContext.remove_provider_for_display(
                Gdk.Display.get_default(), self.current_css_provider)

        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_USER + 1
        )
        self.current_css_provider = css_provider

        self.emit("preset-reload", object())
        self.is_ready = True

    def load_preset_action(self, _unused, *args):
        def load_quick_preset():
            if args[0].get_string().startswith("custom-"):
                self.load_preset_from_file(
                    os.path.join(
                        presets_dir,
                        args[0].get_string().replace("custom-", "", 1)
                    )
                )
            else:
                self.load_preset_from_resource(
                    f"{rootdir}/presets/" + args[0].get_string() + ".json"
                )

        if self.is_dirty:
            dialog, preset_entry = self.construct_unsaved_dialog()

            def on_unsaved_dialog_response(_widget, response, preset_entry):
                if response == "save":
                    self.preset.save_to_file(preset_entry.get_text(), self.plugins_list)
                    self.clear_dirty()
                    load_quick_preset()
                elif response == "discard":
                    self.clear_dirty()
                    load_quick_preset()

            dialog.connect("response", on_unsaved_dialog_response, preset_entry)

            dialog.present()
        else:
            load_quick_preset()

            Gio.SimpleAction.set_state(self.lookup_action("load_preset"), args[0])

    def show_apply_color_scheme_dialog(self, *_args):
        dialog = GradienceAppTypeDialog(
            self.win,
            _("Apply This Color Scheme?"),
            _(
                "Warning: any custom CSS files for those app types will be "
                "irreversibly overwritten!"
            ),
            "apply",
            _("_Apply"),
            Adw.ResponseAppearance.SUGGESTED
        )

        dialog.connect("response", self.apply_color_scheme)
        dialog.present()

    def show_save_preset_dialog(self, *_args):
        dialog = GradienceSaveDialog(self.win, path=os.path.join(
                presets_dir,
                "user",
                to_slug_case(self.preset_name) + ".json"
            )
        )

        preset_entry = dialog.preset_entry
        preset_entry.set_text(self.preset_name)

        preset_entry.connect("changed", self.on_save_preset_entry_change, dialog, preset_entry)
        dialog.connect("response", self.on_save_dialog_response, preset_entry)

        dialog.present()

    def construct_unsaved_dialog(self, *_args):
        dialog = GradienceSaveDialog(
            self.win,
            heading=_("You have unsaved changes!"),
            path=os.path.join(
                presets_dir,
                "user",
                to_slug_case(self.preset_name) + ".json"
            ),
            discard=True
        )

        preset_entry = dialog.preset_entry
        preset_entry.set_text(self.preset_name)

        preset_entry.connect("changed", self.on_save_preset_entry_change, dialog, preset_entry)

        return dialog, preset_entry

    def show_unsaved_dialog(self, *_args):
        dialog, preset_entry = self.construct_unsaved_dialog()

        dialog.connect("response", self.on_save_dialog_response, preset_entry)

        dialog.present()

    def on_save_preset_entry_change(self, _widget, dialog, preset_entry):
        if len(preset_entry.get_text()) == 0:
            dialog.set_body(
                dialog.body.format(
                    os.path.join(
                        presets_dir,
                        "user"
                    )
                )
            )
            dialog.set_response_enabled("save", False)
        else:
            dialog.set_body(
                dialog.body.format(
                    os.path.join(
                        presets_dir,
                        "user",
                        to_slug_case(preset_entry.get_text()) + ".json"
                    )
                )
            )
            dialog.set_response_enabled("save", True)

    def on_save_dialog_response(self, _widget, response, preset_entry):
        if response == "save":
            self.preset.save_to_file(preset_entry.get_text(), self.plugins_list)
            self.clear_dirty()
            self.win.toast_overlay.add_toast(
                Adw.Toast(title=_("Preset saved")))
        elif response == "discard":
            self.clear_dirty()
            self.win.close()

    def apply_color_scheme(self, widget, response):
        if response == "apply":
            if widget.get_app_types()["gtk4"]:
                PresetUtils().apply_preset("gtk4", self.preset)

            if widget.get_app_types()["gtk3"]:
                PresetUtils().apply_preset("gtk3", self.preset)

            self.reload_plugins()
            self.plugins_list.apply()

            self.win.toast_overlay.add_toast(
                Adw.Toast(title=_("Preset has been set. Log out to apply changes."))
            )

    def show_preferences(self, *_args):
        prefs = GradiencePreferencesWindow(self.win)
        prefs.present()

    def show_about_window(self, *_args):
        about = GradienceAboutWindow(self.win)
        about.show_about()

    def update_custom_css_text(self, app_type, new_value):
        self.custom_css[app_type] = new_value
        self.reload_variables()

    def setup_plugins(self):
        logging.debug("setup plugins")

        self.plugins_group = self.plugins_list.to_group()

        self.win.content_plugins.add(self.plugins_group)
        self.plugins_group = self.plugins_group

        self.custom_css_group = GradienceCustomCSSGroup(self.win)

        for app_type in preset_schema["custom_css_app_types"]:
            self.custom_css[app_type] = ""

        self.custom_css_group.load_custom_css(self.custom_css)
        self.win.content_plugins.add(self.custom_css_group)
        self.custom_css_group = self.custom_css_group

        plugins_errors = self.plugins_list.validate()

        self.props.active_window.update_errors(
            self.global_errors + plugins_errors)

    def reload_plugins(self):
        self.plugins_list.reload()
        logging.debug("reload plugins")

        self.win.content_plugins.remove(self.plugins_group)
        self.win.content_plugins.remove(self.custom_css_group)

        self.plugins_group = self.plugins_list.to_group()

        self.win.content_plugins.add(self.plugins_group)
        self.plugins_group = self.plugins_group

        self.custom_css_group = GradienceCustomCSSGroup(self.win)

        for app_type in preset_schema["custom_css_app_types"]:
            self.custom_css[app_type] = ""

        self.custom_css_group.load_custom_css(self.custom_css)
        self.win.content_plugins.add(self.custom_css_group)
        self.custom_css_group = self.custom_css_group

        plugins_errors = self.plugins_list.validate()

        self.props.active_window.update_errors(
            self.global_errors + plugins_errors)


def main():
    """The application's entry point."""
    app = GradienceApplication()
    return app.run(sys.argv)
