# window.py
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

from .constants import rootdir


@Gtk.Template(resource_path=f"{rootdir}/ui/app_type_dialog.ui")
class GradienceAppTypeDialog(Adw.MessageDialog):
    __gtype_name__ = "GradienceAppTypeDialog"

    gtk4_app_type = Gtk.Template.Child("gtk4-app-type")
    gtk3_app_type = Gtk.Template.Child("gtk3-app-type")
    dark = Gtk.Template.Child("dark")
    light = Gtk.Template.Child("light")

    def __init__(
        self,
        heading,
        body,
        ok_response_name,
        ok_response_label,
        ok_response_appearance,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.set_heading(heading)
        self.set_body(body)

        self.add_response("cancel", _("Cancel"))
        self.add_response(ok_response_name, ok_response_label)
        self.set_response_appearance(ok_response_name, ok_response_appearance)
        self.set_default_response("cancel")
        self.set_close_response("cancel")

    def get_app_types(self):
        return {
            "gtk4": self.gtk4_app_type.get_active(),
            "gtk3": self.gtk3_app_type.get_active(),
        }

    def get_color_mode(self):
        return {
            "dark": self.dark.get_active(),
            "light": self.light.get_active(),
        }
