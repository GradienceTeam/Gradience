# presets_manager_window.py
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

from gi.repository import Gtk, Adw, Gio, Gdk
from .constants import rootdir, build_type
import os
import json


@Gtk.Template(resource_path=f"{rootdir}/ui/presets_manager_window.ui")
class GradiencePresetWindow(Adw.Window):
    __gtype_name__ = "GradiencePresetWindow"

    content = Gtk.Template.Child()
    content_explore = Gtk.Template.Child()
    main_view = Gtk.Template.Child()
    toast_overlay = Gtk.Template.Child()
    import_button = Gtk.Template.Child("import-button")

    custom_presets = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setup_pref_group()

    def setup_pref_group(self):
        preset_directory = os.path.join(
            os.environ.get("XDG_CONFIG_HOME", os.environ["HOME"] + "/.config"),
            "presets",
        )
        if not os.path.exists(preset_directory):
            os.makedirs(preset_directory)

        self.custom_presets.clear()
        for file_name in os.listdir(preset_directory):
            if file_name.endswith(".json"):
                try:
                    with open(
                        os.path.join(preset_directory, file_name), "r", encoding="utf-8"
                    ) as file:
                        preset_text = file.read()
                    preset = json.loads(preset_text)
                    if preset.get("variables") is None:
                        raise KeyError("variables")
                    if preset.get("palette") is None:
                        raise KeyError("palette")
                    self.custom_presets[file_name.replace(
                        ".json", "")] = preset["name"]
                except Exception:
                    self.win.toast_overlay.add_toast(
                        Adw.Toast(title=_("Failed to load preset"))
                    )
        self.preset_list = Adw.PreferencesGroup()
        for preset, preset_name in self.custom_presets.items():
            row = Adw.ActionRow()
            row.set_title(preset_name)
            self.preset_list.add(row)
        self.content.add(self.preset_list)
