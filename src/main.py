# main.py
#
# Change the look of Adwaita, with ease
# Copyright (C) 2022  Adwaita Manager Team
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

import sys
import json
import os
import re
import traceback

from anyascii import anyascii

import gi
from gi.repository import Gtk, Gdk, Gio, Adw, GLib, Xdp, XdpGtk4
from material_color_utilities_python import *

from .settings_schema import settings_schema
from .window import AdwcustomizerMainWindow
from .palette_shades import AdwcustomizerPaletteShades
from .option import AdwcustomizerOption
from .app_type_dialog import AdwcustomizerAppTypeDialog
from .custom_css_group import AdwcustomizerCustomCSSGroup
from .plugins_list import AdwcustomizerPluginsList

def to_slug_case(non_slug):
    return re.sub(r"[^0-9a-z]+", "-", anyascii(non_slug).lower()).strip("-")


class AdwcustomizerApplication(Adw.Application):
    """The main application singleton class."""

    def __init__(self, version):
        super().__init__(
            application_id="com.github.AdwCustomizerTeam.AdwCustomizer",
            flags=Gio.ApplicationFlags.FLAGS_NONE,
        )
        self.version = version

        self.portal = Xdp.Portal()

        self.preset_name = ""
        self.is_dirty = False

        self.variables = {}
        self.pref_variables = {}

        self.palette = {}
        self.pref_palette_shades = {}

        self.custom_css = {}
        self.custom_css_group = None

        self.custom_presets = {}
        self.global_errors = []
        self.current_css_provider = None

        self.is_ready = False

    def do_activate(self):
        """Called when the application is activated.

        We raise the application's main window, creating it if
        necessary.
        """

        self.win = self.props.active_window
        if not self.win:
            self.win = AdwcustomizerMainWindow(application=self)

        self.create_action("open_preset_directory", self.open_preset_directory)
        self.create_stateful_action(
            "load_preset",
            GLib.VariantType.new("s"),
            GLib.Variant("s", "adwaita"),
            self.load_preset_action,
        )
        self.create_action("apply_color_scheme",
                           self.show_apply_color_scheme_dialog)
        self.create_action("reset_color_scheme",
                           self.show_reset_color_scheme_dialog)
        self.create_action("save_preset", self.show_save_preset_dialog)
        self.create_action("about", self.show_about_window)

        self.reload_user_defined_presets()
        self.load_preset_from_resource(
            "/com/github/AdwCustomizerTeam/AdwCustomizer/presets/adwaita.json"
        )

        self.win.present()

    def reload_user_defined_presets(self):
        if self.props.active_window.presets_menu.get_n_items() > 1:
            self.props.active_window.presets_menu.remove(1)

        preset_directory = os.path.join(
            os.environ.get("XDG_CONFIG_HOME", os.environ["HOME"] + "/.config" ), "presets")
        if not os.path.exists(preset_directory):
            os.makedirs(preset_directory)

        self.custom_presets.clear()
        for file_name in os.listdir(preset_directory):
            if file_name.endswith(".json"):
                try:
                    with open(
                        os.path.join(preset_directory, file_name), "r", encoding="utf-8"
                    ) as file:
                        preset_text = file.read()
                    preset = json.loads(preset_text)
                    if preset.get("variables") is None:
                        raise KeyError("variables")
                    if preset.get("palette") is None:
                        raise KeyError("palette")
                    self.custom_presets[file_name.replace(
                        ".json", "")] = preset["name"]
                except Exception:
                    self.global_errors.append(
                        {
                            "error": _("Failed to load preset"),
                            "element": file_name,
                            "line": traceback.format_exc().strip(),
                        }
                    )
                    self.win.toast_overlay.add_toast(Adw.Toast(title=_("Failed to load preset")))

                    self.props.active_window.update_errors(self.global_errors)

        custom_menu_section = Gio.Menu()
        for preset, preset_name in self.custom_presets.items():
            menu_item = Gio.MenuItem()
            menu_item.set_label(preset_name)
            if not preset.startswith("error"):
                menu_item.set_action_and_target_value(
                    "app.load_preset", GLib.Variant("s", "custom-" + preset)
                )
            else:
                menu_item.set_action_and_target_value("")
            custom_menu_section.append_item(menu_item)
        open_in_file_manager_item = Gio.MenuItem()
        open_in_file_manager_item.set_label(_("Open in File Manager"))
        open_in_file_manager_item.set_action_and_target_value(
            "app.open_preset_directory"
        )
        custom_menu_section.append_item(open_in_file_manager_item)
        self.props.active_window.presets_menu.append_section(
            _("User Defined Presets"), custom_menu_section
        )

    def open_preset_directory(self, *_args):
        parent = XdpGtk4.parent_new_gtk(self.props.active_window)

        def open_dir_callback(_, result):
            self.portal.open_uri_finish(result)

        self.portal.open_uri(
            parent,
            "file://" + os.path.join(os.environ.get("XDG_CONFIG_HOME", os.environ["HOME"] + "/.config" ), "presets"),
            Xdp.OpenUriFlags.NONE,
            None,
            open_dir_callback,
        )

    def load_preset_from_file(self, preset_path):
        preset_text = ""
        with open(preset_path, "r", encoding="utf-8") as file:
            preset_text = file.read()
        self.load_preset_variables(json.loads(preset_text))

    def load_preset_from_resource(self, preset_path):
        preset_text = Gio.resources_lookup_data(
            preset_path, 0).get_data().decode()
        self.load_preset_variables(json.loads(preset_text))

    def load_preset_variables(self, preset):
        self.is_ready = False

        self.preset_name = preset["name"]
        self.variables = preset["variables"]
        self.palette = preset["palette"]
        if "custom_css" in preset:
            self.custom_css = preset["custom_css"]
        else:
            for app_type in settings_schema["custom_css_app_types"]:
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

    def update_theme_from_monet(self, theme, tone):
        palettes = theme["palettes"]

        palette = {}
        i = 0
        for color in palettes.values():
            i += 1
            palette[str(i)] = hexFromArgb(color.tone(int(tone.get_string())))

        print(palette)

        self.pref_palette_shades["monet"].update_shades(palette)

    def generate_gtk_css(self, app_type):
        final_css = ""
        for key in self.variables.keys():
            final_css += f"@define-color {key} {self.variables[key]};\n"
        for prefix_key in self.palette.keys():
            for key in self.palette[prefix_key].keys():
                final_css += f"@define-color {prefix_key + key} {self.palette[prefix_key][key]};\n"
        final_css += self.custom_css.get(app_type, "")
        return final_css

    def mark_as_dirty(self):
        self.is_dirty = True
        self.props.active_window.save_preset_button.get_child().set_icon_name(
            "disk-unsaved-symbolic"
        )
        self.props.active_window.save_preset_button.get_child().set_tooltip_text(
            _("Unsaved changes")
        )

    def clear_dirty(self):
        self.is_dirty = False
        self.props.active_window.save_preset_button.get_child().set_icon_name(
            "disk-saved-symbolic"
        )
        self.props.active_window.save_preset_button.get_child().set_label("")

    def reload_variables(self):
        parsing_errors = []
        gtk_css = self.generate_gtk_css("gtk4")
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
                    else "<last line>",
                }
            )

        css_provider.connect("parsing-error", on_error)
        css_provider.load_from_data(gtk_css.encode())
        self.props.active_window.update_errors(
            self.global_errors + parsing_errors)
        # loading with the priority above user to override the applied config
        if self.current_css_provider is not None:
            Gtk.StyleContext.remove_provider_for_display(
                Gdk.Display.get_default(), self.current_css_provider
            )
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_USER + 1,
        )
        self.current_css_provider = css_provider

        self.is_ready = True

    def load_preset_action(self, _unused, *args):
        if args[0].get_string().startswith("custom-"):
            self.load_preset_from_file(
                os.path.join(
                    os.environ.get("XDG_CONFIG_HOME", os.environ["HOME"] + "/.config" ),
                    "presets",
                    args[0].get_string().replace("custom-", "", 1) + ".json",
                )
            )
        else:
            self.load_preset_from_resource(
                "/com/github/AdwCustomizerTeam/AdwCustomizer/presets/"
                + args[0].get_string()
                + ".json"
            )
        Gio.SimpleAction.set_state(self.lookup_action("load_preset"), args[0])

    def show_apply_color_scheme_dialog(self, *_args):
        dialog = AdwcustomizerAppTypeDialog(
            _("Apply this color scheme?"),
            _(
                "Warning: any custom CSS files for those app types will be irreversibly overwritten!"
            ),
            "apply",
            _("Apply"),
            Adw.ResponseAppearance.SUGGESTED,
            transient_for=self.props.active_window,
        )
        dialog.connect("response", self.apply_color_scheme)
        dialog.present()

    def show_reset_color_scheme_dialog(self, *_args):
        dialog = AdwcustomizerAppTypeDialog(
            _("Reset applied color scheme?"),
            _("Make sure you have the current settings saved as a preset."),
            "reset",
            _("Reset"),
            Adw.ResponseAppearance.DESTRUCTIVE,
            transient_for=self.props.active_window,
        )
        dialog.connect("response", self.reset_color_scheme)
        dialog.present()

    def show_save_preset_dialog(self, *_args):
        dialog = Adw.MessageDialog(
            transient_for=self.props.active_window,
            heading=_("Save preset as..."),
            body=_(
                "Saving preset to <tt>{0}</tt>. If that preset already exists, it will be overwritten!"
            ).format(
                os.path.join(
                    os.environ.get("XDG_CONFIG_HOME", os.environ["HOME"] + "/.config" ),
                    "presets",
                    to_slug_case(self.preset_name) + ".json",
                )
            ),
            body_use_markup=True,
        )

        dialog.add_response("cancel", _("Cancel"))
        dialog.add_response("save", _("Save"))
        dialog.set_response_appearance(
            "save", Adw.ResponseAppearance.SUGGESTED)
        dialog.set_default_response("cancel")
        dialog.set_close_response("cancel")

        preset_entry = Gtk.Entry(placeholder_text="Preset Name")
        preset_entry.set_text(self.preset_name)

        def on_preset_entry_change(*_args):
            if len(preset_entry.get_text()) == 0:
                dialog.set_body(
                    _(
                        "Saving preset to <tt>{0}</tt>. If that preset already exists, it will be overwritten!"
                    ).format(os.path.join(os.environ.get("XDG_CONFIG_HOME", os.environ["HOME"] + "/.config" ), "presets"))
                )
                dialog.set_response_enabled("save", False)
            else:
                dialog.set_body(
                    _(
                        "Saving preset to <tt>{0}</tt>. If that preset already exists, it will be overwritten!"
                    ).format(
                        os.path.join(
                           os.environ.get("XDG_CONFIG_HOME", os.environ["HOME"] + "/.config" ),
                            "presets",
                            to_slug_case(preset_entry.get_text()) + ".json",
                        )
                    )
                )
                dialog.set_response_enabled("save", True)

        preset_entry.connect("changed", on_preset_entry_change)
        dialog.set_extra_child(preset_entry)

        dialog.connect("response", self.save_preset, preset_entry)

        dialog.present()

    def save_preset(self, _unused, response, entry):
        if response == "save":
            with open(
                os.path.join(
                    os.environ.get("XDG_CONFIG_HOME", os.environ["HOME"] + "/.config" ),
                    "presets",
                    to_slug_case(entry.get_text()) + ".json",
                ),
                "w",
                encoding="utf-8",
            ) as file:
                object_to_write = {
                    "name": entry.get_text(),
                    "variables": self.variables,
                    "palette": self.palette,
                    "custom_css": self.custom_css,
                }
                file.write(json.dumps(object_to_write, indent=4))
                self.clear_dirty()
                self.win.toast_overlay.add_toast(Adw.Toast(title=_("Scheme successfully saved!")))

    def apply_color_scheme(self, widget, response):
        if response == "apply":
            if widget.get_app_types()["gtk4"]:
                gtk4_dir = os.path.join(
                    os.environ.get("XDG_CONFIG_HOME", os.environ["HOME"] + "/.config" ), "gtk-4.0")
                if not os.path.exists(gtk4_dir):
                    os.makedirs(gtk4_dir)
                gtk4_css = self.generate_gtk_css("gtk4")
                with open(
                    os.path.join(gtk4_dir, "gtk.css"), "w", encoding="utf-8"
                ) as file:
                    file.write(gtk4_css)
            if widget.get_app_types()["gtk3"]:
                gtk3_dir = os.path.join(
                    os.environ.get("XDG_CONFIG_HOME", os.environ["HOME"] + "/.config" ), "gtk-3.0")
                if not os.path.exists(gtk3_dir):
                    os.makedirs(gtk3_dir)
                gtk3_css = self.generate_gtk_css("gtk3")
                with open(
                    os.path.join(gtk3_dir, "gtk.css"), "w", encoding="utf-8"
                ) as file:
                    file.write(gtk3_css)
            self.win.toast_overlay.add_toast(Adw.Toast(title=_("Scheme set successfully!")))

    def reset_color_scheme(self, widget, response):
        if response == "reset":
            if widget.get_app_types()["gtk4"]:
                file = Gio.File.new_for_path(
                    os.path.join(
                        os.environ.get("XDG_CONFIG_HOME", os.environ["HOME"] + "/.config" ), "gtk-4.0/gtk.css")
                )
                try:
                    file.delete()
                except Exception:
                    pass
                
            if widget.get_app_types()["gtk3"]:
                file = Gio.File.new_for_path(
                    os.path.join(
                        os.environ.get("XDG_CONFIG_HOME", os.environ["HOME"] + "/.config" ), "gtk-3.0/gtk.css")
                )
                try:
                    file.delete()
                except Exception:
                    pass
            self.win.toast_overlay.add_toast(Adw.Toast(title=_("Reset successfully!")))

    def show_about_window(self, *_args):
        about = Adw.AboutWindow(
            transient_for=self.props.active_window,
            application_name=_("Adwaita Manager"),
            application_icon="com.github.AdwCustomizerTeam.AdwCustomizer",
            developer_name=_("Adwaita Manager Team"),
            website="https://github.com/AdwCustomizerTeam/AdwCustomizer",
            support_url="https://github.com/orgs/AdwCustomizerTeam/discussions",
            issue_url="https://github.com/AdwCustomizerTeam/AdwCustomizer/issues",
            developers=[
                'Artyom "ArtyIF" Fomin https://github.com/ArtyIF',
                "0xMRTT https://github.com/0xMRTT",
                "Verantor https://github.com/Verantor",
            ],
            artists=[
                'David "Daudix UFO" Lapshin https://github.com/daudix-UFO'
            ],
            designers=[
                'David "Daudix UFO" Lapshin https://github.com/daudix-UFO'
            ],
            # Translators: This is a place to put your credits (formats: "Name https://example.com" or "Name <email@example.com>", no quotes) and is not meant to be translated literally.
            translator_credits="""Maxime V https://www.transifex.com/user/profile/Adaoh/
                FineFindus https://github.com/FineFindus
                Karol Lademan https://www.transifex.com/user/profile/karlod/
                Monty Monteusz https://www.transifex.com/user/profile/MontyQIQI/
                Renato Corrêa https://www.transifex.com/user/profile/renatocrrs/
                Aggelos Tselios https://www.transifex.com/user/profile/AndroGR/
                David "Daudix UFO" Lapshin https://github.com/daudix-UFO'
                0xMRTT https://github.com/0xMRTT
                Juanjo Cillero https://www.transifex.com/user/profile/renux918/
                Taylan Tatlı https://www.transifex.com/user/profile/TaylanTatli34/""",
            copyright="© 2022 Adwaita Manager Team",
            license_type=Gtk.License.MIT_X11,
        )
        about.present()

    def update_custom_css_text(self, app_type, new_value):
        self.custom_css[app_type] = new_value
        self.reload_variables()

    def create_action(self, name, callback, shortcuts=None):
        """Add an application action.

        Args:
            name: the name of the action
            callback: the function to be called when the action is
              activated
            shortcuts: an optional list of accelerators
        """
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)

    def create_stateful_action(
        self, name, parameter_type, initial_state, callback, shortcuts=None
    ):
        """Add a stateful application action."""
        action = Gio.SimpleAction.new_stateful(
            name, parameter_type, initial_state)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)


def main(version):
    """The application's entry point."""
    app = AdwcustomizerApplication(version)
    return app.run(sys.argv)
