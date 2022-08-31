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

import time

from gi.repository import Gtk, Adw, Gio, Gdk, Glib

from .run_async import RunAsync
from .modules.utils import buglog
from .constants import rootdir


@Gtk.Template(resource_path=f"{rootdir}/ui/welcome.ui")
class GradienceWelcomeWindow(Adw.Window):
    __gtype_name__ = "GradienceWelcomeWindow"

    settings = Gtk.Settings.get_default()

    carousel = Gtk.Template.Child()
    btn_close = Gtk.Template.Child()
    btn_back = Gtk.Template.Child()
    btn_next = Gtk.Template.Child()
    btn_install = Gtk.Template.Child()
    progressbar = Gtk.Template.Child()
    page_welcome = Gtk.Template.Child()
    page_gradience = Gtk.Template.Child()
    page_configure = Gtk.Template.Child()
    page_download = Gtk.Template.Child()
    page_finish = Gtk.Template.Child()
    img_welcome = Gtk.Template.Child()
    label_skip = Gtk.Template.Child()
    switch_system = Gtk.Template.Child()
    switch_adw_gtk3 = Gtk.Template.Child()

    carousel_pages = [
        "welcome",
        "gradience",
        "configure",
        "download",
        "finish"
    ]
    images = [
        f"{rootdir}/images/welcome.svg",
        f"{rootdir}/images/welcome-dark.svg",
    ]

    def __init__(self, window, **kwargs) -> None:
        super().__init__(**kwargs)
        self.set_transient_for(window)

        # common variables and references
        self.window = window

        # connect signals
        self.connect("close-request", self.quit)
        self.carousel.connect('page-changed', self.page_changed)
        self.btn_close.connect("clicked", self.close_window)
        self.btn_back.connect("clicked", self.previous_page)
        self.btn_next.connect("clicked", self.next_page)
        self.btn_install.connect("clicked", self.install_runner)
        self.settings.connect(
            "notify::gtk-application-prefer-dark-theme",
            self.theme_changed)

        self.btn_close.set_sensitive(False)

        if self.settings.get_property("gtk-application-prefer-dark-theme"):
            self.img_welcome.set_from_resource(self.images[1])

        self.page_changed()

    def theme_changed(self, settings, key):
        self.img_welcome.set_from_resource(
            self.images[settings.get_property("gtk-application-prefer-dark-theme")])

    def get_page(self, index):
        return self.carousel_pages[index]

    def page_changed(self, widget=False, index=0, *_args):
        """
        This function is called on first load and when the user require
        to change the page. It sets the widgets' status according to
        the step of the onboard progress.
        """
        page = self.get_page(index)

        if page == "finish":
            self.btn_back.set_visible(False)
            self.btn_next.set_visible(False)
        elif page == "download":
            self.btn_back.set_visible(True)
            self.btn_next.set_visible(False)
            self.btn_install.set_visible(True)
        elif page == "welcome":
            self.btn_back.set_visible(False)
            self.btn_next.set_visible(True)
        else:
            self.btn_back.set_visible(True)
            self.btn_next.set_visible(True)

    @staticmethod
    def quit(widget=False):
        quit()

    def check_adw_gtk3(self):
        buglog("check if adw-gtk3 installed")
        return True

    def adw_gtk3(self):
        if not self.check_adw_gtk3():  # install
            buglog("install adw-gtk3")

    def get_user_path(self):
        user_path = GLib.getenv('FLATPAK_USER_DIR')
        if user_path:
            return user_path
        else:
            user_data_dir = GLib.get_user_data_dir()
            if not user_data_dir:
                user_data_dir = GLib.getenv('HOST_XDG_DATA_HOME')
                if not user_data_dir:
                    user_data_dir = os.path.expanduser('~/.local/share')
            return os.path.join(user_data_dir, 'flatpak')
        
    def configure_system(self):
        print(self.get_user_path())
        buglog("configure system")

    def install_runner(self, widget):
        def set_completed(result, error=False):
            self.label_skip.set_visible(False)
            self.btn_close.set_sensitive(True)
            self.window.settings.set_boolean("first-run", False)
            self.next_page()

        self.installing = True
        self.btn_back.set_visible(False)
        self.btn_next.set_visible(False)
        self.btn_install.set_visible(False)
        self.progressbar.set_visible(True)
        self.carousel.set_allow_long_swipes(False)
        self.carousel.set_allow_mouse_drag(False)
        self.carousel.set_allow_scroll_wheel(False)
        self.set_deletable(False)

        def install():
            print("install")
            if self.switch_adw_gtk3.get_active():
                print("gtk3")
                self.adw_gtk3()

            if self.switch_system.get_active():
                print("system")
                self.configure_system()

        RunAsync(self.pulse)
        RunAsync(
            install,
            callback=set_completed,
        )

    def previous_page(self, widget=False):
        index = int(self.carousel.get_position())
        previous_page = self.carousel.get_nth_page(index - 1)
        self.carousel.scroll_to(previous_page, True)

    def next_page(self, widget=False):
        index = int(self.carousel.get_position())
        next_page = self.carousel.get_nth_page(index + 1)
        self.carousel.scroll_to(next_page, True)

    def pulse(self):
        # This function update the progress bar every 1s.
        while True:
            time.sleep(.5)
            self.progressbar.pulse()

    def close_window(self, widget):
        self.destroy()
        self.window.present()
