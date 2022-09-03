# repo_row.py
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
from .modules.utils import to_slug_case, buglog


@Gtk.Template(resource_path=f"{rootdir}/ui/repo_row.ui")
class GradienceRepoRow(Adw.ActionRow):
    __gtype_name__ = "GradienceRepoRow"

    remove_button = Gtk.Template.Child("remove_button")

    def __init__(self, repo, repo_name, win, deletable=True, **kwargs):
        super().__init__(**kwargs)

        self.name = repo_name

        self.set_name(repo_name)
        self.set_title(repo_name)
        self.set_subtitle(repo)

        self.app = Gtk.Application.get_default()
        self.win = win
        self.toast_overlay = self.win.toast_overlay

        if not deletable:
            self.remove_button.set_visible(False)

    @Gtk.Template.Callback()
    def on_remove_button_clicked(self, *_args):
        self.toast_overlay.add_toast(
            Adw.Toast(title=_("Repository removed"))
        )

        self.win.remove_repo(self.name)

        self.win.reload_repos_group()
