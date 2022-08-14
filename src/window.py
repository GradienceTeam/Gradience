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

from gi.repository import Gtk, Adw, Gio, Gdk
from .error import AdwcustomizerError
from .settings_schema import settings_schema
from .palette_shades import AdwcustomizerPaletteShades
from .option import AdwcustomizerOption
from .app_type_dialog import AdwcustomizerAppTypeDialog
from .custom_css_group import AdwcustomizerCustomCSSGroup
from material_color_utilities_python import *
from .constants import rootdir, build_type


@Gtk.Template(resource_path=f"{rootdir}/ui/window.ui")
class AdwcustomizerMainWindow(Adw.ApplicationWindow):
    __gtype_name__ = "GradienceMainWindow"

    content = Gtk.Template.Child()
    toast_overlay = Gtk.Template.Child()
    content_monet = Gtk.Template.Child("content_monet")
    content_plugins = Gtk.Template.Child("content_plugins")
    save_preset_button = Gtk.Template.Child("save-preset-button")
    main_menu = Gtk.Template.Child("main-menu")
    presets_dropdown = Gtk.Template.Child("presets-dropdown")
    presets_menu = Gtk.Template.Child("presets-menu")
    errors_button = Gtk.Template.Child("errors-button")
    errors_list = Gtk.Template.Child("errors-list")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.presets_dropdown.get_popover().connect(
            "show", self.on_presets_dropdown_activate
        )

        # Set devel style
        if build_type == "debug":
            self.get_style_context().add_class("devel")

        self.setup_monet_page()
        self.setup_plugins_page()
        self.setup_colors_page()

        self.settings = Gio.Settings("com.github.AdwCustomizerTeam.AdwCustomizer")

        self.settings.bind(
            "window-width", self, "default-width", Gio.SettingsBindFlags.DEFAULT
        )

        self.settings.bind(
            "window-height", self, "default-height", Gio.SettingsBindFlags.DEFAULT
        )
        self.settings.bind(
            "window-maximized", self, "maximized", Gio.SettingsBindFlags.DEFAULT
        )

        self.settings.bind(
            "window-fullscreen", self, "fullscreened", Gio.SettingsBindFlags.DEFAULT
        )

    def on_file_picker_button_clicked(self, *args):
        self.monet_file_chooser_dialog.show()

    def on_monet_file_chooser_response(self, widget, response):
        if response == Gtk.ResponseType.ACCEPT:
            self.monet_image_file = self.monet_file_chooser_dialog.get_file()
            image_basename = self.monet_image_file.get_basename()
            self.monet_file_chooser_button.set_label(image_basename)
        self.monet_file_chooser_dialog.hide()

        if response == Gtk.ResponseType.ACCEPT:
            self.monet_img = Image.open(self.monet_image_file.get_path())
            self.theme = themeFromImage(self.monet_img)
            self.tone = self.tone_row.get_selected_item()
            self.monet_theme = self.monet_theme_row.get_selected_item()
            self.get_application().update_theme_from_monet(
                self.theme, self.tone, self.monet_theme
            )

    def setup_monet_page(self):

        self.monet_pref_group = Adw.PreferencesGroup()
        self.monet_pref_group.set_name("monet")
        self.monet_pref_group.set_title(_("Monet Engine"))
        self.monet_pref_group.set_description(
            _(
                "Monet is an engine that generates Material Design 3 palette from backgrounds color. The generation can be slow"
            )
        )

        self.monet_file_chooser_row = Adw.ActionRow()
        self.monet_file_chooser_row.set_title(_("Background Image"))

        self.monet_file_chooser_dialog = Gtk.FileChooserNative()
        self.monet_file_chooser_dialog.set_transient_for(self)

        self.monet_file_chooser_button = Gtk.Button()
        self.monet_file_chooser_button.set_label(_("Choose a file"))
        self.monet_file_chooser_button.set_icon_name("folder-pictures-symbolic")

        self.monet_file_chooser_button.connect(
            "clicked", self.on_file_picker_button_clicked
        )
        self.monet_file_chooser_dialog.connect(
            "response", self.on_monet_file_chooser_response
        )
        self.monet_file_chooser_row.add_suffix(self.monet_file_chooser_button)
        self.monet_pref_group.add(self.monet_file_chooser_row)

        self.monet_palette_shades = AdwcustomizerPaletteShades(
            "monet", "Monet Palette", 6
        )
        self.get_application().pref_palette_shades["monet"] = self.monet_palette_shades
        self.monet_pref_group.add(self.monet_palette_shades)

        self.tone_row = Adw.ComboRow()
        self.tone_row.set_title(_("Tone"))

        store = Gtk.StringList()
        store_values = []
        for i in range(20, 80, 5):
            store_values.append(str(i))
        for v in store_values:
            store.append(v)
        self.tone_row.set_model(store)
        self.monet_pref_group.add(self.tone_row)

        self.monet_theme_row = Adw.ComboRow()
        self.monet_theme_row.set_title(_("Theme"))

        store = Gtk.StringList()
        store.append("Auto")
        store.append("Dark")
        store.append("Light")
        self.monet_theme_row.set_model(store)
        self.monet_pref_group.add(self.monet_theme_row)

        self.content_monet.add(self.monet_pref_group)

    def setup_plugins_page(self):
        custom_css_group = AdwcustomizerCustomCSSGroup()
        for app_type in settings_schema["custom_css_app_types"]:
            self.get_application().custom_css[app_type] = ""
        custom_css_group.load_custom_css(self.get_application().custom_css)
        self.content_plugins.add(custom_css_group)
        self.get_application().custom_css_group = custom_css_group

    def setup_colors_page(self):
        for group in settings_schema["groups"]:
            pref_group = Adw.PreferencesGroup()
            pref_group.set_name(group["name"])
            pref_group.set_title(group["title"])
            pref_group.set_description(group["description"])

            for variable in group["variables"]:
                pref_variable = AdwcustomizerOption(
                    variable["name"],
                    variable["title"],
                    variable.get("explanation"),
                    variable["adw_gtk3_support"],
                )
                pref_group.add(pref_variable)
                self.get_application().pref_variables[variable["name"]] = pref_variable

            self.content.add(pref_group)

        palette_pref_group = Adw.PreferencesGroup()
        palette_pref_group.set_name("palette_colors")
        palette_pref_group.set_title(_("Palette Colors"))
        palette_pref_group.set_description(
            _(
                'Named palette colors used by some applications. Default colors follow the <a href="https://developer.gnome.org/hig/reference/palette.html">GNOME Human Interface Guidelines</a>.'
            )
        )
        for color in settings_schema["palette"]:
            palette_shades = AdwcustomizerPaletteShades(
                color["prefix"], color["title"], color["n_shades"]
            )
            palette_pref_group.add(palette_shades)
            self.get_application().pref_palette_shades[color["prefix"]] = palette_shades
        self.content.add(palette_pref_group)

    def update_errors(self, errors):
        child = self.errors_list.get_row_at_index(0)
        while child is not None:
            self.errors_list.remove(child)
            child = self.errors_list.get_row_at_index(0)
        self.errors_button.set_visible(len(errors) > 0)
        for error in errors:
            self.errors_list.append(
                AdwcustomizerError(error["error"], error["element"], error["line"])
            )

    def on_presets_dropdown_activate(self, *args):
        self.get_application().reload_user_defined_presets()
