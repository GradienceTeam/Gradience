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
import shutil
import json
from .preset_row import GradiencePresetRow
from .builtin_preset_row import GradienceBuiltinPresetRow


@Gtk.Template(resource_path=f"{rootdir}/ui/presets_manager_window.ui")
class GradiencePresetWindow(Adw.Window):
    __gtype_name__ = "GradiencePresetWindow"

    installed = Gtk.Template.Child("installed")
    explore = Gtk.Template.Child("explore")
    main_view = Gtk.Template.Child()
    toast_overlay = Gtk.Template.Child()

    import_button = Gtk.Template.Child("import_button")
    remove_button = Gtk.Template.Child("remove_button")
    file_manager_button = Gtk.Template.Child("file_manager_button")

    custom_presets = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.setup_explore()

        self.builtin_preset_list = Adw.PreferencesGroup()
        self.builtin_preset_list.set_title(_("Builtin Presets"))
        self.installed.add(self.builtin_preset_list)

        self.preset_list = Adw.PreferencesGroup()
        self.preset_list.set_title(_("User Presets"))
        self.installed.add(self.preset_list)

        self.reload_pref_group()

        self.app = Gtk.Application.get_default()
        self.setup_import()

    def setup_import(self):
        self.file_chooser_dialog = Gtk.FileChooserNative()
        self.file_chooser_dialog.set_transient_for(self)

        self.file_chooser_dialog.connect(
            "response", self.on_file_chooser_response
        )
        
    def setup_explore(self):
        self.explore_list = Adw.PreferencesGroup()
        self.explore_list.set_title(_("Explore community presets"))
        self.explore_list.set_description(_("See <a href=\"https://github.com/GradienceTeam/Gradience\">GradienceTeam/Gradience</a> on Github for more presets"))
        
        empty = Adw.ActionRow()
        empty.set_title(_("Not available yet"))
        
        self.explore_list.add(empty)
        
        self.explore.add(self.explore_list)

    @Gtk.Template.Callback()
    def on_file_manager_button_clicked(self, *_args):
        self.app.open_preset_directory()

    @Gtk.Template.Callback()
    def on_import_button_clicked(self, *_args):
        self.file_chooser_dialog.show()

    def on_file_chooser_response(self, widget, response):
        if response == Gtk.ResponseType.ACCEPT:
            self.preset_path = self.file_chooser_dialog.get_file()
            preset_file = self.preset_path.get_basename()
        self.file_chooser_dialog.hide()

        if response == Gtk.ResponseType.ACCEPT:
            if preset_file.endswith(".json"):

                if preset_file.strip(".json") in self.custom_presets:
                    self.toast_overlay.add_toast(
                        Adw.Toast(title=_("Preset already exists"))
                    )
                else:
                    shutil.copy(self.preset_path.get_path(), os.path.join(
                        os.environ.get("XDG_CONFIG_HOME",
                                       os.environ["HOME"] + "/.config"),
                        "presets",
                        preset_file
                    ))
                    self.toast_overlay.add_toast(
                        Adw.Toast(title=_("Succesfuly imported preset"))
                    )
            else:
                self.toast_overlay.add_toast(
                    Adw.Toast(title=_("Unsupported file format, must be .json"))
                )

        self.reload_pref_group()

    def reload_pref_group(self):
        preset_directory = os.path.join(
            os.environ.get("XDG_CONFIG_HOME", os.environ["HOME"] + "/.config"),
            "presets",
        )
        if not os.path.exists(preset_directory):
            os.makedirs(preset_directory)

        self.custom_presets.clear()
        self.builtin_presets = {
            "adwaita-dark": "Adwaita Dark",
            "adwaita": "Adwaita",
            "pretty-purple": "Pretty Purple",
        }
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
                    self.toast_overlay.add_toast(
                        Adw.Toast(title=_("Failed to load preset"))
                    )
        self.installed.remove(self.preset_list)
        self.installed.remove(self.builtin_preset_list)

        self.builtin_preset_list = Adw.PreferencesGroup()
        self.builtin_preset_list.set_title(_("Builtin Presets"))
        for preset, preset_name in self.builtin_presets.items():
            row = GradienceBuiltinPresetRow(preset_name, self.toast_overlay)
            self.builtin_preset_list.add(row)
        self.installed.add(self.builtin_preset_list)

        self.preset_list = Adw.PreferencesGroup()
        self.preset_list.set_title(_("User Presets"))
        self.preset_list.set_description(_("See <a href=\"https://github.com/GradienceTeam/Gradience\">GradienceTeam/Gradience</a> on Github for more presets"))
        for preset, preset_name in self.custom_presets.items():
            row = GradiencePresetRow(preset_name, self.toast_overlay)
            self.preset_list.add(row)
        self.installed.add(self.preset_list)
