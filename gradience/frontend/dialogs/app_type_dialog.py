# app_type_dialog.py
#
# Change the look of Adwaita, with ease
# Copyright (C) 2022-2023, Gradience Team
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


@Gtk.Template(resource_path=f"{rootdir}/ui/app_type_dialog.ui")
class GradienceAppTypeDialog(Adw.MessageDialog):
    __gtype_name__ = "GradienceAppTypeDialog"

    gtk4_app_type = Gtk.Template.Child("gtk4-app-type")
    gtk3_app_type = Gtk.Template.Child("gtk3-app-type")

    def __init__(self, parent, heading, body, ok_res_name, ok_res_label, ok_res_appearance, **kwargs):
        super().__init__(**kwargs)

        self.parent = parent
        self.app = self.parent.get_application()

        if isinstance(self.parent, Gtk.Window):
            self.win = self.parent
        else:
            self.win = self.app.get_active_window()

        self.set_transient_for(self.win)

        self.set_heading(heading)
        self.set_body(body)

        self.add_response("cancel", _("_Cancel"))
        self.add_response(ok_res_name, ok_res_label)
        self.set_response_appearance(ok_res_name, ok_res_appearance)
        self.set_default_response("cancel")
        self.set_close_response("cancel")

    def get_app_types(self):
        return {
            "gtk4": self.gtk4_app_type.get_active(),
            "gtk3": self.gtk3_app_type.get_active()
        }
