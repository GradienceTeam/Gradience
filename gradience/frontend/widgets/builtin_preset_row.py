# builtin_preset_row.py
#
# Change the look of Adwaita, with ease
# Copyright (C) 2022-2023 Gradience Team
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

from gradience.backend.utils.common import to_slug_case
from gradience.backend.constants import rootdir

from gradience.backend.logger import Logger

logging = Logger()


@Gtk.Template(resource_path=f"{rootdir}/ui/builtin_preset_row.ui")
class GradienceBuiltinPresetRow(Adw.ActionRow):
    __gtype_name__ = "GradienceBuiltinPresetRow"

    def __init__(self, name, toast_overlay, author="", **kwargs):
        super().__init__(**kwargs)

        self.name = name

        self.set_name(name)
        self.set_title(name)

        self.app = Gtk.Application.get_default()

        self.toast_overlay = toast_overlay

    def show_unsaved_dialog(self, *_args):
        dialog, preset_entry = self.app.construct_unsaved_dialog()

        def on_unsaved_dialog_response(_widget, response, preset_entry):
            if response == "save":
                self.app.preset.save_to_file(preset_entry.get_text(), self.app.plugins_list)
                self.app.clear_dirty()
                self.app.load_preset_from_resource(
                    f"{rootdir}/presets/" + to_slug_case(self.name) + ".json"
                )
            elif response == "discard":
                self.app.clear_dirty()
                self.app.load_preset_from_resource(
                    f"{rootdir}/presets/" + to_slug_case(self.name) + ".json"
                )

        dialog.connect("response", on_unsaved_dialog_response, preset_entry)

        dialog.present()

    @Gtk.Template.Callback()
    def on_apply_button_clicked(self, *_args):
        logging.debug("apply")

        if self.app.is_dirty:
            self.show_unsaved_dialog()
        else:
            self.app.load_preset_from_resource(
                f"{rootdir}/presets/" + to_slug_case(self.name) + ".json"
            )
