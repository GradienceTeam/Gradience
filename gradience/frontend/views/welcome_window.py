# welcome_window.py
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

import sys
import time

from gi.repository import Gtk, Adw, Gio

from gradience.frontend.utils.run_async import RunAsync
from gradience.backend.flatpak_overrides import create_gtk_user_override
from gradience.backend.constants import rootdir, app_id, rel_ver

from gradience.backend.logger import Logger

logging = Logger()


@Gtk.Template(resource_path=f"{rootdir}/ui/welcome_window.ui")
class GradienceWelcomeWindow(Adw.Window):
    __gtype_name__ = "GradienceWelcomeWindow"

    settings = Gtk.Settings.get_default()

    carousel = Gtk.Template.Child()

    btn_close = Gtk.Template.Child()
    btn_back = Gtk.Template.Child()
    btn_next = Gtk.Template.Child()
    btn_agree = Gtk.Template.Child()

    img_welcome = Gtk.Template.Child()

    carousel_pages = [
        "welcome",  # 0
        "release",  # 1
        "agreement",  # 2
        "finish",  # 3
    ]

    page_welcome = Gtk.Template.Child()
    page_release = Gtk.Template.Child()

    def __init__(self, window, update=False, **kwargs) -> None:
        super().__init__(**kwargs)

        self.set_transient_for(window)

        self.update = update

        # common variables and references
        self.window = window

        self.gio_settings = Gio.Settings(app_id)

        # connect signals
        self.carousel.connect("page-changed", self.page_changed)
        self.btn_close.connect("clicked", self.close_window)
        self.btn_back.connect("clicked", self.previous_page)
        self.btn_next.connect("clicked", self.next_page)
        self.btn_agree.connect("clicked", self.agree)
        self.connect("close-request", self.quit)

        if self.update:
            self.page_welcome.set_title(_("Thanks for updating Gradience!"))

        self.page_release.set_title(f"Gradience {rel_ver}")

        self.page_changed()

    def get_page(self, index):
        return self.carousel_pages[index]

    def page_changed(self, widget=False, index=0, *_args):
        """
        This function is called on first load and when the user require
        to change the page. It sets the widgets status according to
        the step of the onboard progress.
        """
        page = self.get_page(index)

        self.carousel.set_interactive(True)
        if page == "finish":
            self.btn_next.set_visible(False)
        elif page == "agreement":
            self.btn_back.set_visible(True)
            self.btn_next.set_visible(False)
            self.btn_agree.set_visible(True)
            self.carousel.set_interactive(False)
        elif page == "welcome":
            self.btn_back.set_visible(False)
            self.btn_next.set_visible(True)
        else:
            self.btn_back.set_visible(True)
            self.btn_next.set_visible(True)
            self.carousel.set_interactive(True)

    def agree(self, widget):
        self.window.last_opened_version = self.window.settings.set_string(
            "last-opened-version", rel_ver
        )

        if self.update:
            self.btn_close.set_sensitive(True)
            self.next_page()
        else:
            self.next_page()

    def quit(self, *args):
        self.destroy()
        sys.exit()

    def previous_page(self, widget=False, index=None):
        if index is None:
            index = int(self.carousel.get_position())

        previous_page = self.carousel.get_nth_page(index - 1)
        self.carousel.scroll_to(previous_page, True)

    def next_page(self, widget=False, index=None):
        if index is None:
            index = int(self.carousel.get_position())

        next_page = self.carousel.get_nth_page(index + 1)
        self.carousel.scroll_to(next_page, True)

    def close_window(self, widget):
        self.destroy()
        self.window.present()
