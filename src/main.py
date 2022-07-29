# main.py
#
# Copyright 2022 Adwaita Manager Team
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE X CONSORTIUM BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# Except as contained in this notice, the name(s) of the above copyright
# holders shall not be used in advertising or otherwise to promote the sale,
# use or other dealings in this Software without prior written
# authorization.

import sys
import json
import os
import re
import traceback

from anyascii import anyascii

import gi
from gi.repository import Gtk, Gdk, Gio, Adw, GLib, Xdp, XdpGtk4

from .settings_schema import settings_schema
from .window import AdwcustomizerMainWindow
from .palette_shades import AdwcustomizerPaletteShades
from .option import AdwcustomizerOption
from .app_type_dialog import AdwcustomizerAppTypeDialog
from .custom_css_group import AdwcustomizerCustomCSSGroup

def to_slug_case(non_slug):
    return re.sub(r"[^0-9a-z]+", "-", anyascii(non_slug).lower()).strip("-")

class AdwcustomizerApplication(Adw.Application):
    """The main application singleton class."""

    def __init__(self, version):
        super().__init__(application_id='com.github.ArtyIF.AdwCustomizer',
                         flags=Gio.ApplicationFlags.FLAGS_NONE)
        self.version = version

        self.portal = Xdp.Portal()

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

        win = self.props.active_window
        if not win:
            win = AdwcustomizerMainWindow(application=self)

        for group in settings_schema["groups"]:
            pref_group = Adw.PreferencesGroup()
            pref_group.set_name(group["name"])
            pref_group.set_title(group["title"])
            pref_group.set_description(group["description"])

            for variable in group["variables"]:
                pref_variable = AdwcustomizerOption(variable["name"],
                                                    variable["title"],
                                                    variable["adw_gtk3_support"],
                                                    variable.get("explanation"))
                pref_group.add(pref_variable)
                self.pref_variables[variable["name"]] = pref_variable

            win.content.add(pref_group)

        palette_pref_group = Adw.PreferencesGroup()
        palette_pref_group.set_name("palette_colors")
        palette_pref_group.set_title(_("Palette Colors"))
        palette_pref_group.set_description(_("Named palette colors used by some applications. Default colors follow the <a href=\"https://developer.gnome.org/hig/reference/palette.html\">GNOME Human Interface Guidelines</a>."))
        for color in settings_schema["palette"]:
            palette_shades = AdwcustomizerPaletteShades(color["prefix"],
                                                        color["title"],
                                                        color["n_shades"])
            palette_pref_group.add(palette_shades)
            self.pref_palette_shades[color["prefix"]] = palette_shades
        win.content.add(palette_pref_group)

        self.custom_css_group = AdwcustomizerCustomCSSGroup()
        for app_type in settings_schema["custom_css_app_types"]:
            self.custom_css[app_type] = ""
        self.custom_css_group.load_custom_css(self.custom_css)
        win.content.add(self.custom_css_group)

        preset_directory = os.path.join(os.environ['XDG_CONFIG_HOME'], "presets")
        if not os.path.exists(preset_directory):
            os.makedirs(preset_directory)

        self.load_preset_from_resource('/com/github/ArtyIF/AdwCustomizer/presets/adwaita.json')

        self.create_action("open_preset_directory", self.open_preset_directory)
        self.create_stateful_action("load_preset", GLib.VariantType.new('s'), GLib.Variant('s', 'adwaita'), self.load_preset_action)
        self.create_action("apply_color_scheme", self.show_apply_color_scheme_dialog)
        self.create_action("reset_color_scheme", self.show_reset_color_scheme_dialog)
        self.create_action("save_preset", self.show_save_preset_dialog)
        self.create_action("about", self.show_about_window)

        for file_name in os.listdir(os.environ['XDG_CONFIG_HOME'] + "/presets/"):
            if file_name.endswith(".json"):
                try:
                    with open(os.environ['XDG_CONFIG_HOME'] + "/presets/" + file_name, 'r', encoding="utf-8") as file:
                        preset_text = file.read()
                    preset = json.loads(preset_text)
                    if preset.get('variables') is None:
                        raise KeyError('variables')
                    if preset.get('palette') is None:
                        raise KeyError('palette')
                    self.custom_presets[file_name.replace('.json', '')] = preset['name']
                except Exception as ex:
                    self.global_errors.append({
                        "error": _("Failed to load preset"),
                        "element": file_name,
                        "line": traceback.format_exc().strip()
                    })
                    self.props.active_window.update_errors(self.global_errors)

        custom_menu_section = Gio.Menu()
        for preset, preset_name in self.custom_presets.items():
            menu_item = Gio.MenuItem()
            menu_item.set_label(preset_name)
            if not preset.startswith("error"):
                menu_item.set_action_and_target_value("app.load_preset", GLib.Variant('s', "custom-" + preset))
            else:
                menu_item.set_action_and_target_value("")
            custom_menu_section.append_item(menu_item)
        open_in_file_manager_item = Gio.MenuItem()
        open_in_file_manager_item.set_label(_("Open in File Manager"))
        open_in_file_manager_item.set_action_and_target_value("app.open_preset_directory")
        # does not work yet for some reason, i asked people in flatpak matrix room
        custom_menu_section.append_item(open_in_file_manager_item)
        win.presets_menu.append_section(_("User Defined Presets"), custom_menu_section)
        win.present()

        self.is_ready = True

    def open_preset_directory(self, *_args):
        parent = XdpGtk4.parent_new_gtk(self.props.active_window)
        def open_dir_callback(_, result):
            self.portal.open_uri_finish(result)
        self.portal.open_uri(
            parent,
            "file://" + os.environ['XDG_CONFIG_HOME'] + "/presets/",
            Xdp.OpenUriFlags.NONE,
            None,
            open_dir_callback
        )

    def load_preset_from_file(self, preset_path):
        preset_text = ""
        with open(preset_path, 'r', encoding="utf-8") as file:
            preset_text = file.read()
        self.load_preset_variables(json.loads(preset_text))

    def load_preset_from_resource(self, preset_path):
        preset_text = Gio.resources_lookup_data(preset_path, 0).get_data().decode()
        self.load_preset_variables(json.loads(preset_text))

    def load_preset_variables(self, preset):
        self.props.active_window.set_current_preset_name(preset["name"])
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

        self.reload_variables()

    def generate_gtk_css(self, app_type):
        final_css = ""
        for key in self.variables.keys():
            final_css += f"@define-color {key} {self.variables[key]};\n"
        for prefix_key in self.palette.keys():
            for key in self.palette[prefix_key].keys():
                final_css += f"@define-color {prefix_key + key} {self.palette[prefix_key][key]};\n"
        final_css += self.custom_css.get(app_type, "")
        return final_css

    def reload_variables(self):
        parsing_errors = []
        gtk_css = self.generate_gtk_css("gtk4")
        css_provider = Gtk.CssProvider()
        def on_error(_, section, error):
            start_location = section.get_start_location().chars
            end_location = section.get_end_location().chars
            line_number = section.get_end_location().lines
            parsing_errors.append({
                "error": error.message,
                "element": gtk_css[start_location:end_location].strip(),
                "line": gtk_css.splitlines()[line_number] if line_number < len(gtk_css.splitlines()) else "<last line>"
            })
        css_provider.connect("parsing-error", on_error)
        css_provider.load_from_data(gtk_css.encode())
        self.props.active_window.update_errors(self.global_errors + parsing_errors)
        # loading with the priority above user to override the applied config
        if self.current_css_provider is not None:
            Gtk.StyleContext.remove_provider_for_display(Gdk.Display.get_default(), self.current_css_provider)
        Gtk.StyleContext.add_provider_for_display(Gdk.Display.get_default(), css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER + 1)
        self.current_css_provider = css_provider

    def load_preset_action(self, _unused, *args):
        if args[0].get_string().startswith("custom-"):
            self.load_preset_from_file(os.environ['XDG_CONFIG_HOME'] + "/presets/" + args[0].get_string().replace("custom-", "", 1) + ".json")
        else:
            self.load_preset_from_resource('/com/github/ArtyIF/AdwCustomizer/presets/' + args[0].get_string() + '.json')
        Gio.SimpleAction.set_state(self.lookup_action("load_preset"), args[0])

    def show_apply_color_scheme_dialog(self, *_args):
        dialog = AdwcustomizerAppTypeDialog(_("Apply this color scheme?"),
                                            _("Warning: any custom CSS files for those app types will be irreversibly overwritten!"),
                                            "apply", _("Apply"), Adw.ResponseAppearance.SUGGESTED,
                                            transient_for=self.props.active_window)
        dialog.connect("response", self.apply_color_scheme)
        dialog.present()

    def show_reset_color_scheme_dialog(self, *_args):
        dialog = AdwcustomizerAppTypeDialog(_("Reset applied color scheme?"),
                                            _("Make sure you have the current settings saved as a preset."),
                                            "reset", _("Reset"), Adw.ResponseAppearance.DESTRUCTIVE,
                                            transient_for=self.props.active_window)
        dialog.connect("response", self.reset_color_scheme)
        dialog.present()

    def show_save_preset_dialog(self, *_args):
        dialog = Adw.MessageDialog(transient_for=self.props.active_window,
                                   heading=_("Save preset as..."),
                                   body=_("Saving preset to <tt>{0}</tt>. If that preset already exists, it will be overwritten!").format(os.environ['XDG_CONFIG_HOME'] + "/presets/"),
                                   body_use_markup=True)

        dialog.add_response("cancel", _("Cancel"))
        dialog.add_response("save", _("Save"))
        dialog.set_response_appearance("save", Adw.ResponseAppearance.SUGGESTED)
        dialog.set_response_enabled("save", False)
        dialog.set_default_response("cancel")
        dialog.set_close_response("cancel")

        preset_entry = Gtk.Entry(placeholder_text="Preset Name")
        def on_preset_entry_change(*_args):
            if len(preset_entry.get_text()) == 0:
                dialog.set_body(_("Saving preset to <tt>{0}</tt>. If that preset already exists, it will be overwritten!").format(os.environ['XDG_CONFIG_HOME'] + "/presets/"))
                dialog.set_response_enabled("save", False)
            else:
                dialog.set_body(_("Saving preset to <tt>{0}</tt>. If that preset already exists, it will be overwritten!").format(os.environ['XDG_CONFIG_HOME'] + "/presets/" + to_slug_case(preset_entry.get_text()) + ".json"))
                dialog.set_response_enabled("save", True)
        preset_entry.connect("changed", on_preset_entry_change)
        dialog.set_extra_child(preset_entry)

        dialog.connect("response", self.save_preset, preset_entry)

        dialog.present()

    def save_preset(self, _unused, response, entry):
        if response == "save":
            with open(os.environ['XDG_CONFIG_HOME'] + "/presets/" + to_slug_case(entry.get_text()) + ".json", 'w', encoding="utf-8") as file:
                object_to_write = {
                    "name": entry.get_text(),
                    "variables": self.variables,
                    "palette": self.palette,
                    "custom_css": self.custom_css
                }
                file.write(json.dumps(object_to_write, indent=4))

    def apply_color_scheme(self, widget, response):
        if response == "apply":
            if widget.get_app_types()["gtk4"]:
                gtk4_css = self.generate_gtk_css("gtk4")
                with open(os.environ['XDG_CONFIG_HOME'] + "/gtk-4.0/gtk.css", 'w', encoding="utf-8") as file:
                    file.write(gtk4_css)
            if widget.get_app_types()["gtk3"]:
                gtk3_css = self.generate_gtk_css("gtk3")
                with open(os.environ['XDG_CONFIG_HOME'] + "/gtk-3.0/gtk.css", 'w', encoding="utf-8") as file:
                    file.write(gtk3_css)

    def reset_color_scheme(self, widget, response):
        if response == "reset":
            if widget.get_app_types()["gtk4"]:
                file = Gio.File.new_for_path(GLib.get_user_config_dir() + "/gtk-4.0/gtk.css")
                try:
                    file.delete()
                except:
                    pass
            if widget.get_app_types()["gtk3"]:
                file = Gio.File.new_for_path(GLib.get_user_config_dir() + "/gtk-3.0/gtk.css")
                try:
                    file.delete()
                except:
                    pass

    def show_about_window(self, *_args):
        about = Adw.AboutWindow(transient_for=self.props.active_window,
                                application_name=_("Adwaita Manager"),
                                application_icon='com.github.ArtyIF.AdwCustomizer',
                                developer_name=_("Adwaita Manager Team"),
                                developers=['Artyom "ArtyIF" Fomin https://github.com/ArtyIF', 'Verantor https://github.com/Verantor'],
                                artists=['David "Daudix UFO" Lapshin https://github.com/daudix-UFO'],
                                translator_credits=_("translator-credits"),
                                copyright='© 2022 Adwaita Manager Team',
                                license_type=Gtk.License.MIT_X11)

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

    def create_stateful_action(self, name, parameter_type, initial_state, callback, shortcuts=None):
        """Add a stateful application action.
        """
        action = Gio.SimpleAction.new_stateful(name, parameter_type, initial_state)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)


def main(version):
    """The application's entry point."""
    app = AdwcustomizerApplication(version)
    return app.run(sys.argv)
