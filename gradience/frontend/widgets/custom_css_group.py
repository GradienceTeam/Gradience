# custom_css_group.py
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

from gi.repository import Gtk, Adw

from gradience.backend.constants import rootdir

from gradience.backend.logger import Logger

logging = Logger()


@Gtk.Template(resource_path=f"{rootdir}/ui/custom_css_group.ui")
class GradienceCustomCSSGroup(Adw.PreferencesGroup):
    __gtype_name__ = "GradienceCustomCSSGroup"

    app_type_dropdown = Gtk.Template.Child("app_type_dropdown")
    custom_css_text_view = Gtk.Template.Child("custom_css_text_view")

    def __init__(self, parent, **kwargs):
        super().__init__(**kwargs)

        self.parent = parent
        self.app = self.parent.get_application()

        self.custom_css = {}

    def load_custom_css(self, custom_css):
        self.custom_css = custom_css

        self.custom_css_text_view.get_buffer().set_text(
            list(self.custom_css.values())[
                self.app_type_dropdown.get_selected()]
        )

    def reset_buffer(self):
        self.app.update_custom_css_text("gtk3", "")
        self.app.update_custom_css_text("gtk4", "")

        self.custom_css_text_view.get_buffer().set_text("")

    @Gtk.Template.Callback()
    def on_custom_css_changed(self, buffer):
        self.app.mark_as_dirty()
        self.app.update_custom_css_text(
            list(self.custom_css.keys())[
                self.app_type_dropdown.get_selected()],
            buffer.props.text
        )

    @Gtk.Template.Callback()
    def on_dropdown_notify(self, _unused, pspec):
        if pspec.name == "selected":
            logging.debug(f"Custom CSS values: {self.custom_css.values()}")
            logging.debug(f"Selected app type in dropdown: {self.app_type_dropdown.get_selected()}")
            self.custom_css_text_view.get_buffer().set_text(
                list(self.custom_css.values())[
                    self.app_type_dropdown.get_selected()]
            )
