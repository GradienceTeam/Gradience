# window.py
#
# Copyright 2022 Gradience Team
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
from .constants import rootdir, build_type
import os
import json

@Gtk.Template(resource_path=f"{rootdir}/ui/presets_manager_window.ui")
class AdwcustomizerPresetWindow(Adw.Window):
    __gtype_name__ = "AdwcustomizerPresetWindow"

    main_view = Gtk.Template.Child()
    toast_overlay = Gtk.Template.Child()
    import_button = Gtk.Template.Child("import-button")
    preset_list = Gtk.Template.Child("preset_list")

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
                    self.custom_presets[file_name.replace(".json", "")] = preset["name"]
                except Exception:
                    self.win.toast_overlay.add_toast(
                        Adw.Toast(title=_("Failed to load preset"))
                    )


        
        for preset, preset_name in self.custom_presets.items():
            row = Adw.ActionRow()
            row.set_title(preset_name)
            self.preset_list.add(row)
        