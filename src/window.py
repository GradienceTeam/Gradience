# window.py
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

from gi.repository import Gtk, Adw
from .error import AdwcustomizerError
from .settings_schema import settings_schema
from .palette_shades import AdwcustomizerPaletteShades
from .option import AdwcustomizerOption
from .app_type_dialog import AdwcustomizerAppTypeDialog
from .custom_css_group import AdwcustomizerCustomCSSGroup

@Gtk.Template(resource_path='/com/github/AdwCustomizerTeam/AdwCustomizer/ui/window.ui')
class AdwcustomizerMainWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'AdwcustomizerMainWindow'

    content = Gtk.Template.Child()
    save_preset_button = Gtk.Template.Child("save-preset-button")
    presets_dropdown = Gtk.Template.Child("presets-dropdown")
    presets_menu = Gtk.Template.Child("presets-menu")
    errors_button = Gtk.Template.Child("errors-button")
    errors_list = Gtk.Template.Child("errors-list")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.presets_dropdown.get_popover().connect("show", self.on_presets_dropdown_activate)

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
                self.get_application().pref_variables[variable["name"]] = pref_variable

            self.content.add(pref_group)

        palette_pref_group = Adw.PreferencesGroup()
        palette_pref_group.set_name("palette_colors")
        palette_pref_group.set_title(_("Palette Colors"))
        palette_pref_group.set_description(_("Named palette colors used by some applications. Default colors follow the <a href=\"https://developer.gnome.org/hig/reference/palette.html\">GNOME Human Interface Guidelines</a>."))
        for color in settings_schema["palette"]:
            palette_shades = AdwcustomizerPaletteShades(color["prefix"],
                                                        color["title"],
                                                        color["n_shades"])
            palette_pref_group.add(palette_shades)
            self.get_application().pref_palette_shades[color["prefix"]] = palette_shades
        self.content.add(palette_pref_group)

        custom_css_group = AdwcustomizerCustomCSSGroup()
        for app_type in settings_schema["custom_css_app_types"]:
            self.get_application().custom_css[app_type] = ""
        custom_css_group.load_custom_css(self.get_application().custom_css)
        self.content.add(custom_css_group)
        self.get_application().custom_css_group = custom_css_group

    def update_errors(self, errors):
        child = self.errors_list.get_row_at_index(0)
        while child is not None:
            self.errors_list.remove(child)
            child = self.errors_list.get_row_at_index(0)
        self.errors_button.set_visible(len(errors) > 0)
        for error in errors:
            self.errors_list.append(AdwcustomizerError(error["error"], error["element"], error["line"]))

    def on_presets_dropdown_activate(self, *args):
        self.get_application().reload_user_defined_presets()
