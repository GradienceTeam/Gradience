# preset_row.py
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

import json
import os

from gi.repository import Gtk, Adw

from gradience.modules.custom_presets import PRESET_DIR

from .constants import rootdir
from .modules.utils import to_slug_case, buglog
from .modules.preset import Preset


@Gtk.Template(resource_path=f"{rootdir}/ui/preset_row.ui")
class GradiencePresetRow(Adw.ActionRow):
    __gtype_name__ = "GradiencePresetRow"

    name_entry = Gtk.Template.Child("name_entry")
    value_stack = Gtk.Template.Child("value_stack")
    name_entry_toggle = Gtk.Template.Child("name_entry_toggle")
    apply_button = Gtk.Template.Child("apply_button")
    remove_button = Gtk.Template.Child("remove_button")

    def __init__(self, name, win, repo_name, author="", **kwargs):
        super().__init__(**kwargs)

        self.name = name
        self.old_name = name

        self.prefix = to_slug_case(repo_name)

        self.set_name(name)
        self.set_title(name)
        self.set_subtitle(author)
        self.name_entry.set_text(name)

        self.app = Gtk.Application.get_default()
        self.win = win
        self.toast_overlay = self.win.toast_overlay

        self.preset = Preset(name, repo_name)

        apply_button = Gtk.Template.Child("apply_button")
        rename_button = Gtk.Template.Child("rename_button")

    @Gtk.Template.Callback()
    def on_apply_button_clicked(self, *_args):
        buglog("apply")

        self.app.load_preset_from_file(
            os.path.join(
                os.environ.get("XDG_CONFIG_HOME",
                               os.environ["HOME"] + "/.config"),
                "presets",
                self.prefix,
                to_slug_case(self.name) + ".json",
            )
        )

    @Gtk.Template.Callback()
    def on_name_entry_changed(self, *_args):
        self.name = self.name_entry.get_text()
        self.set_name(self.name)
        self.set_title(self.name)

    @Gtk.Template.Callback()
    def on_name_entry_toggled(self, *_args):
        if self.name_entry_toggle.get_active():
            self.value_stack.set_visible_child(self.name_entry)
        else:
            self.update_value()
            self.value_stack.set_visible_child(self.apply_button)

    @Gtk.Template.Callback()
    def on_remove_button_clicked(self, *_args):
        self.delete_preset = True
        self.delete_toast = Adw.Toast(title=_("Preset removed"))
        self.delete_toast.set_button_label(_("Undo"))
        self.delete_toast.connect("dismissed", self.on_delete_toast_dismissed)

        self.toast_overlay.add_toast(self.delete_toast)

        self.win.old_name = self.name

        try:
            os.rename(
                os.path.join(
                    os.environ.get("XDG_CONFIG_HOME",
                                   os.environ["HOME"] + "/.config"),
                    "presets",
                    self.prefix,
                    to_slug_case(self.old_name) + ".json",
                ),
                os.path.join(
                    os.environ.get("XDG_CONFIG_HOME",
                                   os.environ["HOME"] + "/.config"),
                    "presets",
                    self.prefix,
                    to_slug_case(self.old_name) + ".json.to_delete",
                ),
            )
            print("rename")
            self.set_name(self.name + "(" + _("Pending deletion") + ")")
            print("renamed")
        except Exception as exception:
            buglog(exception)

        self.delete_preset = True

        # self.win.reload_pref_group()

    def update_value(self):
        self.preset.preset_name = self.name
        self.preset.name = to_slug_case(self.name)
        self.preset.save_preset()
        os.remove(
            os.path.join(
                PRESET_DIR,
                self.prefix,
                to_slug_case(self.old_name) + ".json",
            )
        )
        self.old_name = self.name

    def on_delete_toast_dismissed(self, widget):
        if self.delete_preset:
            try:
                os.remove(
                    os.path.join(
                        os.environ.get(
                            "XDG_CONFIG_HOME", os.environ["HOME"] + "/.config"
                        ),
                        "presets",
                        self.prefix,
                        to_slug_case(self.old_name) + ".json.to_delete",
                    )
                )
            except Exception as exception:
                buglog(exception)
                self.toast_overlay.add_toast(
                    Adw.Toast(title=_("Unable to delete preset"))
                )
            finally:
                self.win.reload_pref_group()
        else:
            try:
                os.rename(
                    os.path.join(
                        os.environ.get(
                            "XDG_CONFIG_HOME", os.environ["HOME"] + "/.config"
                        ),
                        "presets",
                        self.prefix,
                        to_slug_case(self.old_name) + ".json.to_delete",
                    ),
                    os.path.join(
                        os.environ.get(
                            "XDG_CONFIG_HOME", os.environ["HOME"] + "/.config"
                        ),
                        "presets",
                        self.prefix,
                        to_slug_case(self.old_name) + ".json",
                    ),
                )
            except Exception as exception:
                buglog(exception)
            finally:
                self.win.reload_pref_group()

        self.delete_preset = True

    def on_undo_button_clicked(self, *_args):
        self.delete_preset = False
        self.delete_toast.dismiss()
