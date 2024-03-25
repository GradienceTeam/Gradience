# save_dialog.py
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

from gi.repository import Gtk, Adw

from gradience.backend.constants import rootdir


# TODO: Make this dialog async when Libadwaita 1.3 becomes available \
# https://gnome.pages.gitlab.gnome.org/libadwaita/doc/main/method.MessageDialog.choose.html
@Gtk.Template(resource_path=f"{rootdir}/ui/save_dialog.ui")
class GradienceSaveDialog(Adw.MessageDialog):
    __gtype_name__ = "GradienceSaveDialog"

    preset_entry = Gtk.Template.Child("preset-entry")

    def __init__(self, parent, heading=None, body=None, path=None, discard=False, **kwargs):
        super().__init__(**kwargs)

        self.parent = parent
        self.app = self.parent.get_application()

        self.body = _(
            "Saving preset to \n <small><i><tt>{0}</tt></i></small>. \n If that preset already "
            "exists, it will be overwritten."
        )

        if isinstance(self.parent, Gtk.Window):
            self.win = self.parent
        else:
            self.win = self.app.get_active_window()

        self.set_transient_for(self.win)

        if heading:
            self.heading = heading
            self.set_heading(self.heading)

        if not body and path:
            self.set_body(self.body.format(path))
        elif body:
            self.body = body
            self.set_body(self.body)
        elif not body and not path:
            raise AttributeError("DEV FAULT: You need to either specify 'body' or 'path' parameter")

        self.add_response("cancel", _("_Cancel"))

        if discard:
            self.add_response("discard", _("Discard"))
            self.set_response_appearance(
                "discard", Adw.ResponseAppearance.DESTRUCTIVE
            )

        self.add_response("save", _("_Save"))
        self.set_default_response("cancel")
        self.set_close_response("cancel")

        self.set_response_appearance(
            "save", Adw.ResponseAppearance.SUGGESTED
        )

