# main.py
#
# Copyright 2022 ArtyIF
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

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Gdk, Gio, Adw
from .window import AdwcustomizerMainWindow
from .option import AdwcustomizerOption


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
                pref_variable = AdwcustomizerOption(variable["name"], variable["title"], variable.get("explanation"), "#00000000")
                pref_group.add(pref_variable)
                self.pref_variables[variable["name"]] = pref_variable

            win.content.add(pref_group)

        self.load_preset('/com/github/ArtyIF/AdwCustomizer/presets/adwaita.json')

        self.create_action("load_adw_preset", self.load_adw_preset)
        self.create_action("load_adw_dark_preset", self.load_adw_dark_preset)
        self.create_action("about", self.show_about_window)

        win.present()

        self.is_ready = True

    def load_preset(self, preset_path):
        preset_text = Gio.resources_lookup_data(preset_path, 0).get_data().decode()
        preset = json.loads(preset_text)
        self.variables = preset["variables"]

        for key in self.variables.keys():
            if key in self.pref_variables:
                self.pref_variables[key].update_value(self.variables[key])

        self.reload_variables()

    def generate_css(self, variables):
        final_css = ""
        for key in variables.keys():
            final_css += "@define-color {0} {1};\n".format(key, variables[key])
        return final_css

    def reload_variables(self):
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(self.generate_css(self.variables).encode())
        # loading with the priority above user to override the applied config
        Gtk.StyleContext.add_provider_for_display(Gdk.Display.get_default(), css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER + 1)

    def load_adw_preset(self, widget, _):
        self.load_preset('/com/github/ArtyIF/AdwCustomizer/presets/adwaita.json')

    def load_adw_dark_preset(self, widget, _):
        self.load_preset('/com/github/ArtyIF/AdwCustomizer/presets/adwaita-dark.json')

    def show_about_window(self, widget, _):
        # TODO: Adw.AboutWindow doesn't exist in production GNOME Runtime, only master. Replace with this once it becomes available in the stable version
        # about = Adw.AboutWindow(transient_for=self.props.active_window,
        #                         application_name='AdwCustomizer',
        #                         application_icon='com.github.ArtyIF.AdwCustomizer',
        #                         developer_name='ArtyIF',
        #                         version='whatever_version',
        #                         developers=['ArtyIF'],
        #                         copyright='© 2022 ArtyIF')
        about = Gtk.AboutDialog(transient_for=self.props.active_window,
                                modal=True,
                                program_name='AdwCustomizer',
                                logo_icon_name='com.github.ArtyIF.AdwCustomizer',
                                version='0.0.6',
                                authors=['ArtyIF'],
                                copyright='© 2022 ArtyIF')

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


def main(version):
    """The application's entry point."""
    app = AdwcustomizerApplication()
    return app.run(sys.argv)
