# welcome.py
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

from .modules.run_async import RunAsync
from .modules.utils import buglog
from .modules.flatpak_overrides import (
    create_gtk_user_override
)
from .constants import rootdir, app_id, rel_ver


@Gtk.Template(resource_path=f"{rootdir}/ui/welcome.ui")
class GradienceWelcomeWindow(Adw.Window):
    __gtype_name__ = "GradienceWelcomeWindow"

    settings = Gtk.Settings.get_default()

    carousel = Gtk.Template.Child()

    btn_close = Gtk.Template.Child()
    btn_back = Gtk.Template.Child()
    btn_next = Gtk.Template.Child()
    btn_install = Gtk.Template.Child()
    btn_agree = Gtk.Template.Child()

    switch_system = Gtk.Template.Child()
    switch_adw_gtk3 = Gtk.Template.Child()

    progressbar = Gtk.Template.Child()
    img_welcome = Gtk.Template.Child()
    label_skip = Gtk.Template.Child()

    images = [
        f"{rootdir}/images/welcome.svg",
        f"{rootdir}/images/welcome-dark.svg",
    ]

    carousel_pages = [
        "welcome",  # 0
        "release",  # 1
        "agreement",  # 2
        "gradience",  # 3
        "configure",  # 4
        "download",  # 5
        "finish",  # 6
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
        self.btn_install.connect("clicked", self.install_runner)
        self.btn_agree.connect("clicked", self.agree)
        self.settings.connect(
            "notify::gtk-application-prefer-dark-theme", self.theme_changed
        )
        self.connect("close-request", self.quit)

        if self.update:
            self.page_welcome.set_title(_("Thanks for updating Gradience!"))

        self.page_release.set_title(f"Gradience {rel_ver}")

        self.btn_close.set_sensitive(False)

        if self.settings.get_property("gtk-application-prefer-dark-theme"):
            self.img_welcome.set_from_resource(self.images[1])

        self.page_changed()

    def theme_changed(self, settings, key):
        self.img_welcome.set_from_resource(
            self.images[settings.get_property(
                "gtk-application-prefer-dark-theme")]
        )

    def get_page(self, index):
        return self.carousel_pages[index]

    def page_changed(self, widget=False, index=0, *_args):
        """
        This function is called on first load and when the user require
        to change the page. It sets the widgets status according to
        the step of the onboard progress.
        """
        page = self.get_page(index)

        if page == "finish":
            self.btn_back.set_visible(False)
            self.btn_next.set_visible(False)
            self.carousel.set_interactive(False)
        elif page == "agreement":
            self.btn_back.set_visible(True)
            self.btn_next.set_visible(False)
            self.btn_agree.set_visible(True)
            self.carousel.set_interactive(False)
        elif page == "download":
            self.btn_back.set_visible(True)
            self.btn_next.set_visible(False)
            self.btn_install.set_visible(True)
            self.carousel.set_interactive(False)
        elif page == "welcome":
            self.btn_back.set_visible(False)
            self.btn_next.set_visible(True)
            self.carousel.set_interactive(True)
        else:
            self.btn_back.set_visible(True)
            self.btn_next.set_visible(True)
            self.btn_install.set_visible(False)
            self.carousel.set_interactive(True)

    def agree(self, widget):
        self.window.last_opened_version = self.window.settings.set_string(
            "last-opened-version", rel_ver
        )

        if self.update:
            self.btn_close.set_sensitive(True)
            self.label_skip.set_visible(False)
            self.next_page(index=5)
        else:
            self.next_page()

    def quit(self, *args):
        self.destroy()
        sys.exit()

    # TODO: Add adw-gtk3 check
    def check_adw_gtk3(self, *args):
        buglog("check if adw-gtk3 installed")
        return True

    def adw_gtk3(self):
        if not self.check_adw_gtk3():  # install
            buglog("install adw-gtk3")

    def configure_system(self):
        buglog("configure system")
        self.allow_flatpak_theming_user_toggled()

    def allow_flatpak_theming_user_toggled(self, *args):
        create_gtk_user_override(self, self.gio_settings, "gtk4")

    def install_runner(self, widget):
        def set_completed(result, error=False):
            self.label_skip.set_visible(False)
            self.btn_close.set_sensitive(True)
            self.window.settings.set_boolean("first-run", False)
            self.next_page()

        self.installing = True
        self.set_deletable(False)

        def install():
            if self.switch_adw_gtk3.get_active():
                self.adw_gtk3()

            if self.switch_system.get_active():
                self.configure_system()

        RunAsync(self.pulse)
        RunAsync(
            install,
            callback=set_completed,
        )

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

    def pulse(self):
        # This function updates the progress bar every 1s.
        while True:
            time.sleep(0.5)
            self.progressbar.pulse()

    def close_window(self, widget):
        self.destroy()
        self.window.present()
