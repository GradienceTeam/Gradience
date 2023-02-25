# main_window.py
#
# Change the look of Adwaita, with ease
# Copyright (C) 2022  Gradience Team
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

from gi.repository import Gtk, Adw, Gio

from gradience.backend.theming.monet import Monet
from gradience.backend.constants import rootdir, app_id, build_type

from gradience.frontend.widgets.error_list_row import GradienceErrorListRow
from gradience.frontend.widgets.palette_shades import GradiencePaletteShades
from gradience.frontend.widgets.option_row import GradienceOptionRow
from gradience.frontend.settings_schema import settings_schema

from gradience.backend.logger import Logger

logging = Logger()


@Gtk.Template(resource_path=f"{rootdir}/ui/window.ui")
class GradienceMainWindow(Adw.ApplicationWindow):
    __gtype_name__ = "GradienceMainWindow"

    content = Gtk.Template.Child()
    toast_overlay = Gtk.Template.Child()
    content_monet = Gtk.Template.Child("content_monet")
    content_plugins = Gtk.Template.Child("content_plugins")
    save_preset_button = Gtk.Template.Child("save-preset-button")
    main_menu = Gtk.Template.Child("main-menu")
    errors_button = Gtk.Template.Child("errors-button")
    errors_list = Gtk.Template.Child("errors-list")
    presets_dropdown = Gtk.Template.Child("presets-dropdown")
    presets_menu = Gtk.Template.Child("presets-menu")
    monet_image_file = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.app = Gtk.Application.get_default()
        self.settings = Gio.Settings(app_id)

        self.presets_dropdown.get_popover().connect(
            "show", self.on_presets_dropdown_activate
        )

        # Set devel style
        if build_type == "debug":
            self.get_style_context().add_class("devel")

        self.setup_monet_page()
        self.setup_colors_page()

        self.connect("close-request", self.on_close_request)
        self.connect("unrealize", self.save_window_props)

        self.style_manager = self.app.style_manager

    # TODO: Check if org.freedesktop.portal.Settings portal will allow us to \
    # read org.gnome.desktop.background DConf key
    # FIXME: Find purpose for this snippet
    '''def get_default_wallpaper(self):
        background_settings = Gio.Settings("org.gnome.desktop.background")
        if self.style_manager.get_dark():
            picture_uri = background_settings.get_string("picture-uri-dark")
        else:
            picture_uri = background_settings.get_string("picture-uri")
        logging.debug(picture_uri)
        if picture_uri.startswith("file://"):
            self.monet_image_file = Gio.File.new_for_uri(picture_uri)
        else:
            self.monet_image_file = Gio.File.new_for_path(picture_uri)
        image_basename = self.monet_image_file.get_basename()
        logging.debug(image_basename)
        self.monet_image_file = self.monet_image_file.get_path()
        self.monet_file_chooser_button.set_label(image_basename)
        self.monet_file_chooser_button.set_tooltip_text(self.monet_image_file)
        logging.debug(self.monet_image_file)
        # self.on_apply_button() # Comment out for now, because it always shows
        # that annoying toast on startup'''

    def on_file_picker_button_clicked(self, *args):
        self.monet_file_chooser_dialog.show()

    def on_close_request(self, *args):
        if self.app.is_dirty:
            logging.debug("Window close request")
            self.app.show_unsaved_dialog()
            return True
        self.close()

    def save_window_props(self, *args):
        win_size = self.get_default_size()

        self.settings.set_int("window-width", win_size.width)
        self.settings.set_int("window-height", win_size.height)

        self.settings.set_boolean("window-maximized", self.is_maximized())
        self.settings.set_boolean("window-fullscreen", self.is_fullscreen())

    def on_monet_file_chooser_response(self, widget, response):
        if response == Gtk.ResponseType.ACCEPT:
            self.monet_image_file = self.monet_file_chooser_dialog.get_file()
            image_basename = self.monet_image_file.get_basename()
            self.monet_file_chooser_button.set_label(image_basename)
            self.monet_file_chooser_button.set_tooltip_text(image_basename)

        self.monet_file_chooser_dialog.hide()

        if response == Gtk.ResponseType.ACCEPT:
            self.monet_image_file = self.monet_image_file.get_path()
            self.on_apply_button()

    def setup_monet_page(self):
        self.monet_pref_group = Adw.PreferencesGroup()
        self.monet_pref_group.set_name("monet")
        self.monet_pref_group.set_title(_("Monet Engine"))
        self.monet_pref_group.set_description(
            _(
                "Monet is an engine that generates a Material Design 3 "
                "palette from an image's color."
            )
        )

        self.apply_button = Gtk.Button()
        self.apply_button.set_label(_("Apply"))
        self.apply_button.set_valign(Gtk.Align.CENTER)
        self.apply_button.connect("clicked", self.on_apply_button)
        self.apply_button.set_css_classes("suggested-action")

        self.monet_pref_group.set_header_suffix(self.apply_button)

        self.monet_file_chooser_row = Adw.ActionRow()
        self.monet_file_chooser_row.set_title(_("Select an Image"))

        self.monet_file_chooser_dialog = Gtk.FileChooserNative()
        self.monet_file_chooser_dialog.set_title(_("Choose a Image File"))
        self.monet_file_chooser_dialog.set_transient_for(self)
        self.monet_file_chooser_dialog.set_modal(True)

        self.monet_file_chooser_button = Gtk.Button()
        self.monet_file_chooser_button.set_valign(Gtk.Align.CENTER)

        child_button = Gtk.Box()
        label = Gtk.Label()
        label.set_label(_("Choose a File"))
        child_button.append(label)

        icon = Gtk.Image()
        icon.set_from_icon_name("folder-pictures-symbolic")
        child_button.append(icon)
        child_button.set_spacing(10)

        self.monet_file_chooser_button.set_child(child_button)

        self.monet_file_chooser_button.connect(
            "clicked", self.on_file_picker_button_clicked
        )

        self.monet_file_chooser_dialog.connect(
            "response", self.on_monet_file_chooser_response
        )

        self.monet_file_chooser_row.add_suffix(self.monet_file_chooser_button)
        self.monet_pref_group.add(self.monet_file_chooser_row)

        self.monet_palette_shades = GradiencePaletteShades(
            "monet", _("Monet Palette"), 6
        )
        self.app.pref_palette_shades["monet"] = self.monet_palette_shades
        self.monet_pref_group.add(self.monet_palette_shades)

        # FIXME: Comment out for now
        '''self.tone_row = Adw.ComboRow()
        self.tone_row.set_title(_("Tone"))

        store = Gtk.StringList()
        store_values = []
        for i in range(20, 80, 5):
            store_values.append(str(i))
        for v in store_values:
            store.append(v)
        self.tone_row.set_model(store)
        self.monet_pref_group.add(self.tone_row)'''

        self.monet_theme_row = Adw.ComboRow()
        self.monet_theme_row.set_title(_("Theme"))

        store = Gtk.StringList()
        store.append(_("Auto"))
        store.append(_("Light"))
        store.append(_("Dark"))
        self.monet_theme_row.set_model(store)
        self.monet_pref_group.add(self.monet_theme_row)

        self.content_monet.add(self.monet_pref_group)

    def on_apply_button(self, *_args):
        if self.monet_image_file:
            try:
                self.theme = Monet().generate_from_image(self.monet_image_file)

                #self.tone = self.tone_row.get_selected_item()
                self.monet_theme = self.monet_theme_row.get_selected_item()

                self.app.custom_css_group.reset_buffer()

                self.app.update_theme_from_monet(self.theme, self.monet_theme)
            except (OSError, AttributeError, ValueError) as e:
                logging.error("Failed to generate Monet palette.", exc=e)
                self.toast_overlay.add_toast(
                    Adw.Toast(title=_("Failed to generate Monet palette"))
                )
            else:
                self.toast_overlay.add_toast(
                    Adw.Toast(title=_("Palette generated"))
                )
        else:
            self.toast_overlay.add_toast(
                Adw.Toast(title=_("Select a background first"))
            )

    def setup_colors_page(self):
        for group in settings_schema["groups"]:
            pref_group = Adw.PreferencesGroup()
            pref_group.set_name(group["name"])
            pref_group.set_title(group["title"])
            pref_group.set_description(group["description"])

            for variable in group["variables"]:
                pref_variable = GradienceOptionRow(
                    variable["name"],
                    variable["title"],
                    variable.get("explanation"),
                    variable["adw_gtk3_support"],
                )
                pref_group.add(pref_variable)
                self.app.pref_variables[variable["name"]] = pref_variable

            self.content.add(pref_group)

        palette_pref_group = Adw.PreferencesGroup()
        palette_pref_group.set_name("palette_colors")
        palette_pref_group.set_title(_("Palette Colors"))
        palette_pref_group.set_description(
            _(
                "Named palette colors used by some applications. Default "
                "colors follow the "
                '<a href="https://developer.gnome.org/hig/reference/palette.html">'
                "GNOME Human Interface Guidelines</a>."
            )
        )
        for color in settings_schema["palette"]:
            palette_shades = GradiencePaletteShades(
                color["prefix"], color["title"], color["n_shades"]
            )
            palette_pref_group.add(palette_shades)
            self.app.pref_palette_shades[color["prefix"]] = palette_shades
        self.content.add(palette_pref_group)

    def update_errors(self, errors):
        child = self.errors_list.get_row_at_index(0)
        while child is not None:
            self.errors_list.remove(child)
            child = self.errors_list.get_row_at_index(0)
        self.errors_button.set_visible(len(errors) > 0)
        for error in errors:
            self.errors_list.append(
                GradienceErrorListRow(error["error"], error["element"], error["line"])
            )

    def on_presets_dropdown_activate(self, *args):
        self.app.reload_user_defined_presets()
