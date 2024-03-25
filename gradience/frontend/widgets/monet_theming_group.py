# monet_theming_group.py
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

from gi.repository import Gtk, Adw

from gradience.backend.theming.monet import Monet
from gradience.backend.constants import rootdir

from gradience.frontend.widgets.palette_shades import GradiencePaletteShades

from gradience.backend.logger import Logger

logging = Logger()


@Gtk.Template(resource_path=f"{rootdir}/ui/monet_theming_group.ui")
class GradienceMonetThemingGroup(Adw.PreferencesGroup):
    __gtype_name__ = "GradienceMonetThemingGroup"

    monet_theming_expander = Gtk.Template.Child("monet-theming-expander")
    monet_file_chooser = Gtk.Template.Child("monet-file-chooser")
    monet_file_chooser_button = Gtk.Template.Child("file-chooser-button")

    def __init__(self, parent, **kwargs):
        super().__init__(**kwargs)

        self.parent = parent
        self.app = self.parent.get_application()

        self.monet_image_file = None

        self.setup_signals()
        self.setup()

    def setup_signals(self):
        self.monet_file_chooser.connect(
            "response", self.on_monet_file_chooser_response)

    def setup(self):
        self.monet_file_chooser.set_transient_for(self.parent)

        self.setup_palette_shades()
        #self.setup_tone_row()
        self.setup_theme_row()

    def setup_palette_shades(self):
        self.monet_palette_shades = GradiencePaletteShades(
            "monet", _("Palette"), 6
        )
        self.app.pref_palette_shades["monet"] = self.monet_palette_shades

        self.monet_theming_expander.add_row(self.monet_palette_shades)

    # TODO: Rethink how it should be implemented
    '''def setup_tone_row(self):
        self.tone_row = Adw.ComboRow()
        self.tone_row.set_title(_("Tone"))

        tone_store = Gtk.StringList()
        tone_store_values = []

        for i in range(20, 80, 5):
            tone_store_values.append(str(i))

        for v in tone_store_values:
            tone_store.append(v)

        self.tone_row.set_model(tone_store)

        self.monet_theming_expander.add_row(self.tone_row)'''

    def setup_theme_row(self):
        self.theme_row = Adw.ComboRow()
        self.theme_row.set_title(_("Style"))

        theme_store = Gtk.StringList()
        theme_store.append(_("Auto"))
        theme_store.append(_("Light"))
        theme_store.append(_("Dark"))

        self.theme_row.set_model(theme_store)

        self.monet_theming_expander.add_row(self.theme_row)

    @Gtk.Template.Callback()
    def on_apply_button_clicked(self, *_args):
        if self.monet_image_file:
            try:
                monet_theme = Monet().generate_palette_from_image(self.monet_image_file)
                #tone = self.tone_row.get_selected_item().get_string() # TODO: Remove tone requirement from Monet Engine
                variant_pos = self.theme_row.props.selected

                class variantEnum(Enum):
                    AUTO = 0
                    LIGHT = 1
                    DARK = 2

                def __get_variant_string():
                    if variant_pos == variantEnum.AUTO.value:
                        return "auto"
                    elif variant_pos == variantEnum.DARK.value:
                        return "dark"
                    elif variant_pos == variantEnum.LIGHT.value:
                        return "light"

                variant_str = __get_variant_string()

                self.app.custom_css_group.reset_buffer()

                self.app.update_theme_from_monet(monet_theme, variant_str)
            except (OSError, AttributeError, ValueError) as e:
                logging.error("Failed to generate Monet palette", exc=e)
                self.parent.toast_overlay.add_toast(
                    Adw.Toast(title=_("Failed to generate Monet palette"))
                )
            else:
                logging.info("Monet palette generated successfully")
                self.parent.toast_overlay.add_toast(
                    Adw.Toast(title=_("Palette generated"))
                )
        else:
            logging.error("Input image for Monet generation not selected")
            self.parent.toast_overlay.add_toast(
                Adw.Toast(title=_("Select an image first"))
            )

    @Gtk.Template.Callback()
    def on_file_chooser_button_clicked(self, *_args):
        self.monet_file_chooser.show()

    def on_monet_file_chooser_response(self, widget, response):
        if response == Gtk.ResponseType.ACCEPT:
            self.monet_image_file = self.monet_file_chooser.get_file()
            image_basename = self.monet_image_file.get_basename()
            self.monet_file_chooser_button.set_label(image_basename)
            self.monet_file_chooser_button.set_tooltip_text(image_basename)

        self.monet_file_chooser.hide()

        if response == Gtk.ResponseType.ACCEPT:
            self.monet_image_file = self.monet_image_file.get_path()
            self.on_apply_button_clicked()
