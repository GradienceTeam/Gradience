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
import gi
import json
import os
import re
import subprocess

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Gdk, Gio, Adw, GLib
from .window import AdwcustomizerMainWindow
from .option import AdwcustomizerOption

def to_slug_case(non_slug):
    return re.sub(r"[^0-9A-Za-z\u00C0-\uFFFF]+", "-", non_slug.lower())

class AdwcustomizerApplication(Adw.Application):
    """The main application singleton class."""

    def __init__(self):
        super().__init__(application_id='com.github.ArtyIF.AdwCustomizer',
                         flags=Gio.ApplicationFlags.FLAGS_NONE)

    def do_activate(self):
        """Called when the application is activated.

        We raise the application's main window, creating it if
        necessary.
        """
        self.variables = {}
        self.is_ready = False

        win = self.props.active_window
        if not win:
            win = AdwcustomizerMainWindow(application=self)

        settings_schema_text = Gio.resources_lookup_data('/com/github/ArtyIF/AdwCustomizer/settings_schema.json', 0).get_data().decode()
        self.settings_schema = json.loads(settings_schema_text)

        self.pref_variables = {}
        for group in self.settings_schema["groups"]:
            pref_group = Adw.PreferencesGroup()
            pref_group.set_name(group["name"])
            pref_group.set_title(group["title"])
            pref_group.set_description(group["description"])

            for variable in group["variables"]:
                pref_variable = AdwcustomizerOption(variable["name"], variable["title"], variable["adw_gtk3_support"], variable.get("explanation"))
                pref_group.add(pref_variable)
                self.pref_variables[variable["name"]] = pref_variable

            win.content.add(pref_group)

        # usually flatpak takes care of that, but in case it doesn't we do it ourselves
        preset_directory = os.path.join(os.environ['XDG_CONFIG_HOME'], "adwcustomizer", "presets")
        if not os.path.exists(preset_directory):
            os.makedirs(preset_directory)

        self.load_preset_from_resource('/com/github/ArtyIF/AdwCustomizer/presets/adwaita.json')

        self.create_stateful_action("load_preset", GLib.VariantType.new('s'), GLib.Variant('s', 'adwaita'), self.load_preset_action)
        self.create_action("apply_css_file", self.show_apply_css_file_dialog)
        self.create_action("reset_css_file", self.show_reset_css_file_dialog)
        self.create_action("save_preset", self.show_save_preset_dialog)
        self.create_action("about", self.show_about_window)

        self.custom_presets = {}
        for file in os.listdir(os.environ['XDG_CONFIG_HOME'] + "/adwcustomizer/presets/"):
            if file.endswith(".json"):
                try:
                    with open(os.environ['XDG_CONFIG_HOME'] + "/adwcustomizer/presets/" + file, 'r') as f:
                        preset_text = f.read()
                    preset = json.loads(preset_text)
                    self.custom_presets[file.replace('.json', '')] = preset['name']
                except Exception as e:
                    print("Failed to load " + file + ":\n" + str(e))
                    self.custom_presets["error-" + file.replace('.json', '')] = file + " (Failed to Load)"

        custom_menu_section = Gio.Menu()
        for preset in self.custom_presets.keys():
            menu_item = Gio.MenuItem()
            menu_item.set_label(self.custom_presets[preset])
            if not preset.startswith("error"):
                menu_item.set_action_and_target_value("app.load_preset", GLib.Variant('s', "custom-" + preset))
            else:
                menu_item.set_action_and_target_value("")
            custom_menu_section.append_item(menu_item)
        win.presets_menu.append_section("User Defined", custom_menu_section)
        win.present()

        self.is_ready = True

    def load_preset_from_file(self, preset_path):
        preset_text = ""
        with open(preset_path, 'r') as f:
            preset_text = f.read()
        preset = json.loads(preset_text)
        self.props.active_window.set_current_preset_name(preset["name"])

        self.variables = preset["variables"]
        self.load_preset_variables()

    def load_preset_from_resource(self, preset_path):
        preset_text = Gio.resources_lookup_data(preset_path, 0).get_data().decode()
        preset = json.loads(preset_text)
        self.props.active_window.set_current_preset_name(preset["name"])

        self.variables = preset["variables"]
        self.load_preset_variables()

    def load_preset_variables(self):
        for key in self.variables.keys():
            if key in self.pref_variables:
                self.pref_variables[key].update_value(self.variables[key])

        self.reload_variables()

    def generate_css(self):
        final_css = ""
        for key in self.variables.keys():
            final_css += "@define-color {0} {1};\n".format(key, self.variables[key])
        return final_css

    def reload_variables(self):
        parsing_errors = []
        css_provider = Gtk.CssProvider()
        def on_parsing_error(provider, section, error):
            start_location = section.get_start_location().chars
            end_location = section.get_end_location().chars
            line_number = section.get_end_location().lines
            parsing_errors.append({
                "error": error.message,
                "element": self.generate_css()[start_location:end_location],
                "line": self.generate_css().splitlines()[line_number]
            })
        css_provider.connect("parsing-error", on_parsing_error)
        css_provider.load_from_data(self.generate_css().encode())
        self.props.active_window.update_parsing_errors(parsing_errors)
        # loading with the priority above user to override the applied config
        Gtk.StyleContext.add_provider_for_display(Gdk.Display.get_default(), css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER + 1)

    def load_preset_action(self, widget, *args):
        if args[0].get_string().startswith("custom-"):
            self.load_preset_from_file(os.environ['XDG_CONFIG_HOME'] + "/adwcustomizer/presets/" + args[0].get_string().replace("custom-", "", 1) + ".json")
        else:
            self.load_preset_from_resource('/com/github/ArtyIF/AdwCustomizer/presets/' + args[0].get_string() + '.json')
        Gio.SimpleAction.set_state(self.lookup_action("load_preset"), args[0])

    def show_apply_css_file_dialog(self, widget, _):
        dialog = Adw.MessageDialog(transient_for=self.props.active_window,
                                   heading="Apply this color scheme?",
                                   body="If there is a gtk.css file, it will irreversibly be rewritten. Make sure you have the current gtk.css file backed up.")

        dialog.add_response("cancel", "Cancel")
        dialog.add_response("apply", "Apply")
        dialog.set_response_appearance("apply", Adw.ResponseAppearance.SUGGESTED)
        dialog.set_default_response("cancel")
        dialog.set_close_response("cancel")
        dialog.connect("response", self.apply_css_file)

        dialog.present()

    def show_reset_css_file_dialog(self, widget, _):
        dialog = Adw.MessageDialog(transient_for=self.props.active_window,
                                   heading="Reset gtk.css?",
                                   body="This will irreversibly reset the color scheme to default. Make sure you have the current settings saved as a preset.")

        dialog.add_response("cancel", "Cancel")
        dialog.add_response("reset", "Reset")
        dialog.set_response_appearance("reset", Adw.ResponseAppearance.DESTRUCTIVE)
        dialog.set_default_response("cancel")
        dialog.set_close_response("cancel")
        dialog.connect("response", self.reset_css_file)

        dialog.present()

    def show_save_preset_dialog(self, widget, _):
        dialog = Adw.MessageDialog(transient_for=self.props.active_window,
                                   heading="Save preset as...",
                                   body="Saving to <tt>$XDG_CONFIG_HOME/adwcustomizer/presets/</tt>",
                                   body_use_markup=True)

        dialog.add_response("cancel", "Cancel")
        dialog.add_response("save", "Save")
        dialog.set_response_appearance("save", Adw.ResponseAppearance.SUGGESTED)
        dialog.set_response_enabled("save", False)
        dialog.set_default_response("cancel")
        dialog.set_close_response("cancel")

        preset_entry = Gtk.Entry(placeholder_text="Preset Name")
        def on_preset_entry_change(self, *args):
            if len(preset_entry.get_text()) == 0:
                dialog.set_body("Saving to <tt>$XDG_CONFIG_HOME/adwcustomizer/presets/</tt>")
                dialog.set_response_enabled("save", False)
            else:
                dialog.set_body("Saving to <tt>$XDG_CONFIG_HOME/adwcustomizer/presets/" + to_slug_case(preset_entry.get_text()) + ".json</tt>. If that preset already exists, it will be overwritten!")
                dialog.set_response_enabled("save", True)
        preset_entry.connect("changed", on_preset_entry_change)
        dialog.set_extra_child(preset_entry)

        dialog.connect("response", self.save_preset, preset_entry)

        dialog.present()

    def save_preset(self, widget, response, entry):
        if response == "save":
            with open(os.environ['XDG_CONFIG_HOME'] + "/adwcustomizer/presets/" + to_slug_case(entry.get_text()) + ".json", 'w') as f:
                object_to_write = {
                    "name": entry.get_text(),
                    "variables": self.variables
                }
                f.write(json.dumps(object_to_write, indent=4))

    def apply_css_file(self, widget, response):
        if response == "apply":
            with open(os.environ['XDG_CONFIG_HOME'] + "/gtk-4.0/gtk.css", 'w') as f:
                f.write(self.generate_css())
            with open(os.environ['XDG_CONFIG_HOME'] + "/gtk-3.0/gtk.css", 'w') as f:
                f.write(self.generate_css())

    def reset_css_file(self, widget, response):
        if response == "reset":
            file = Gio.File.new_for_path(GLib.get_user_config_dir() + "/gtk-4.0/gtk.css")
            try:
                file.delete()
            except:
                pass
            file = Gio.File.new_for_path(GLib.get_user_config_dir() + "/gtk-3.0/gtk.css")
            try:
                file.delete()
            except:
                pass

    def show_about_window(self, widget, _):
        about = Adw.AboutWindow(transient_for=self.props.active_window,
                                application_name='Adwaita Manager',
                                application_icon='com.github.ArtyIF.AdwCustomizer',
                                developer_name='Adwaita Manager Team',
                                version='0.0.19',
                                developers=['Artyom "ArtyIF" Fomin https://github.com/ArtyIF', 'Verantor https://github.com/Verantor'],
                                copyright='© 2022 Adwaita Manager Team',
                                license_type=Gtk.License.MIT_X11)

        about.present()


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
    app = AdwcustomizerApplication()
    return app.run(sys.argv)
