# explore_preset_row.py
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

from gi.repository import Gtk, Gdk, Adw

from .constants import rootdir
from .modules.custom_presets import download_preset
from .modules.utils import to_slug_case, buglog

@Gtk.Template(resource_path=f"{rootdir}/ui/explore_preset_row.ui")
class GradienceExplorePresetRow(Adw.ActionRow):
    __gtype_name__ = "GradienceExplorePresetRow"

    apply_button = Gtk.Template.Child("apply_button")
    download_button = Gtk.Template.Child("download_button")

    def __init__(self, name, url, win, author="", **kwargs):
        super().__init__(**kwargs)

        self.name = name

        self.set_name(name)
        self.set_title(name)
        self.set_subtitle(author)

        self.app = Gtk.Application.get_default()
        self.win = win
        self.toast_overlay = self.win.toast_overlay

        self.url = url


    @Gtk.Template.Callback()
    def on_apply_button_clicked(self, *_args):
        try:
            download_preset(to_slug_case(self.name), self.url)
        except Exception:
            self.toast_overlay.add_toast(
                Adw.Toast(title=_("Scheme could not be downloaded!"))
            )
        else:
            self.app.load_preset_from_file(os.path.join(
                os.environ.get("XDG_CONFIG_HOME",
                            os.environ["HOME"] + "/.config"),
                "presets",
                to_slug_case(self.name) + ".json",
            ))

            self.toast_overlay.add_toast(
                Adw.Toast(title=_("Scheme successfully downloaded!"))
            )

        buglog("Apply and download compeleted")

    @Gtk.Template.Callback()
    def on_download_button_clicked(self, *_args):
        try:
            download_preset(to_slug_case(self.name), self.url)
        except Exception:
            self.toast_overlay.add_toast(
                Adw.Toast(title=_("Scheme could not be downloaded!"))
            )
        else:
            self.toast_overlay.add_toast(
                Adw.Toast(title=_("Scheme successfully downloaded!"))
            )
        buglog("Download compeleted")
