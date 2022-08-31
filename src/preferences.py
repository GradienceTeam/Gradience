# preferences.py
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

import os

from gi.repository import GLib, Gio, Gtk, Adw

from .constants import rootdir, app_id
from .modules.utils import buglog


@Gtk.Template(resource_path=f"{rootdir}/ui/preferences.ui")
class GradiencePreferencesWindow(Adw.PreferencesWindow):
    __gtype_name__ = "GradiencePreferencesWindow"
    
    allow_flatpak_theming_user = Gtk.Template.Child()
    allow_flatpak_theming_global = Gtk.Template.Child()

    def __init__(self, parent, **kwargs):
        super().__init__(**kwargs)

        self.parent = parent
        self.settings = parent.settings

        self.setup()

    def setup(self):
        self.set_search_enabled(False)

        self.setup_flatpak_group()
        
    def setup_flatpak_group(self):
        user_flatpak_theming = self.settings.get_boolean("user-flatpak-theming")
        #global_flatpak_theming = self.settings.get_boolean("global-flatpak-theming")

        self.allow_flatpak_theming_user.set_state(user_flatpak_theming)
        #self.allow_flatpak_theming_global.set_state(global_flatpak_theming)

        self.allow_flatpak_theming_user.connect("state-set", self.on_allow_flatpak_theming_user_toggled)
        #self.allow_flatpak_theming_global.connect("state-set", self.on_allow_flatpak_theming_global_toggled)


    def get_system_flatpak_path(self):
        systemPath = GLib.getenv("FLATPAK_SYSTEM_DIR")
        buglog(f"systemPath: {systemPath}")
        
        if systemPath:
            return systemPath

        systemDataDir = GLib.build_filenamev([
            GLib.DIR_SEPARATOR_S, "var", "lib"
        ])

        return GLib.build_filenamev([systemDataDir, "flatpak"])

    def get_user_flatpak_path(self):
        userPath = GLib.getenv("FLATPAK_USER_DIR")
        buglog(f"userPath: {userPath}")
        
        if userPath:
            return userPath

        userDataDir = GLib.build_filenamev([
            GLib.get_home_dir(), ".local", "share"
        ])

        return GLib.build_filenamev([userDataDir, "flatpak"])


    def on_allow_flatpak_theming_user_toggled(self, *args):
        user_flatpak_theming = self.settings.get_boolean("user-flatpak-theming")
        state = self.allow_flatpak_theming_user.props.state

        override_dir = os.path.join(self.get_user_flatpak_path(), "overrides")
        filename = GLib.build_filenamev([
            override_dir, "global"
        ])

        user_keyfile = GLib.KeyFile.new()

        if state == False:
            try:
                user_keyfile.load_from_file(filename, GLib.KeyFileFlags.NONE)
            except GLib.GError as e:
                if e.code == 4:
                    buglog("File doesn't exist. Attempting to create one")
                    if not os.path.exists(override_dir):
                        os.makedirs(override_dir)
                        buglog("dir create")

                    file = Gio.File.new_for_path(filename)
                    file.create(Gio.FileCreateFlags.NONE, None)

                    user_keyfile.load_from_file(filename, GLib.KeyFileFlags.NONE)
                    user_keyfile.set_string("Context", "filesystems", "xdg-config/gtk-4.0") 
                #else:
                #    self.add_toast(Adw.Toast(title=_("Unexpected file error occurred")))
                #    buglog(f"Unhandled GLib.FileError error code. Exc: {e}")
            else:
                try:
                    filesys_list = user_keyfile.get_string_list("Context", "filesystems")
                except GLib.GError:
                    user_keyfile.set_string("Context", "filesystems", "xdg-config/gtk-4.0")
                else:
                    if user_keyfile.get_string_list("Context", "filesystems") != filesys_list + ["xdg-config/gtk-4.0"]:
                        user_keyfile.set_string_list("Context", "filesystems", filesys_list + ["xdg-config/gtk-4.0"])
            finally:
                try:
                    user_keyfile.save_to_file(filename)
                except Glib.GError as e:
                    self.add_toast(Adw.Toast(title=_("Failed to save override")))
                    buglog(f"Failed to save keyfile structure to override. Exc: {e}")
                else:
                    self.settings.set_boolean("user-flatpak-theming", True)
                    buglog(f"user-flatpak-theming: {self.settings.get_boolean('user-flatpak-theming')}")
                    #value = user_keyfile.get_string_list("Context", "filesystems")
                    #print(value)
        else:
            try:
                user_keyfile.load_from_file(filename, GLib.KeyFileFlags.NONE)
            except GLib.GError as e:
                if e.code == 4:
                    self.settings.set_boolean("user-flatpak-theming", False)
                    buglog("remove override: File doesn't exist")
                else:
                    self.add_toast(Adw.Toast(title=_("Unexpected file error occurred")))
                    buglog(f"Unhandled GLib.FileError error code. Exc: {e}")
            else:
                try:
                    filesys_list = user_keyfile.get_string_list("Context", "filesystems")
                except GLib.GError:
                    self.settings.set_boolean("user-flatpak-theming", False)
                    buglog("remove override: Group/key not found.")
                else:
                    if "xdg-config/gtk-4.0" in filesys_list:
                        buglog(f"before: {filesys_list}")
                        filesys_list.remove("xdg-config/gtk-4.0")
                        buglog(f"after: {filesys_list}")

                        user_keyfile.set_string_list("Context", "filesystems", filesys_list)
                        try:
                            user_keyfile.save_to_file(filename)
                        except Glib.GError as e:
                            self.add_toast(Adw.Toast(title=_("Failed to save override")))
                            buglog(f"Failed to save keyfile structure to override. Exc: {e}")
                        else:
                            self.settings.set_boolean("user-flatpak-theming", False)
                            buglog("remove override: Value removed.")
                    else:
                        self.settings.set_boolean("user-flatpak-theming", False)
                        buglog("remove override: Value not found.")

            buglog(f"user-flatpak-theming: {self.settings.get_boolean('user-flatpak-theming')}")

    # Do not use this function for now, as it's lacking authentication
    def on_allow_flatpak_theming_global_toggled(self, *args):
        global_flatpak_theming = self.settings.get_boolean("global-flatpak-theming")
        state = self.allow_flatpak_theming_global.props.state

        override_dir = os.path.join(self.get_system_flatpak_path(), "overrides")
        filename = GLib.build_filenamev([
            self.get_system_flatpak_path(), "global"
        ])

        global_keyfile = GLib.KeyFile.new()

        # TODO: Implement user authentication using Polkit
        if state == False:
            try:
                global_keyfile.load_from_file(filename, GLib.KeyFileFlags.NONE)
            except GLib.GError as e:
                if e.code == 4:
                    buglog("File doesn't exist. Attempting to create one")
                    if not os.path.exists(override_dir):
                        try:
                            os.makedirs(override_dir)
                        except Exception as e:
                            buglog(f"Unhandled GLib.FileError error code. Exc: {e}")
                        buglog("dir create")

                    file = Gio.File.new_for_path(filename)
                    file.create(Gio.FileCreateFlags.NONE, None)

                    global_keyfile.load_from_file(filename, GLib.KeyFileFlags.NONE)
                    global_keyfile.set_string("Context", "filesystems", "xdg-config/gtk-4.0") 
                else:
                    self.add_toast(Adw.Toast(title=_("Unexpected file error occurred")))
                    buglog(f"Unhandled GLib.FileError error code. Exc: {e}")
            else:
                try:
                    filesys_list = global_keyfile.get_string_list("Context", "filesystems")
                except GLib.GError:
                    global_keyfile.set_string("Context", "filesystems", "xdg-config/gtk-4.0")
                else:
                    if global_keyfile.get_string_list("Context", "filesystems") != filesys_list + ["xdg-config/gtk-4.0"]:
                        global_keyfile.set_string_list("Context", "filesystems", filesys_list + ["xdg-config/gtk-4.0"])
                        print("here")
            finally:
                try:
                    global_keyfile.save_to_file(filename)
                except Glib.GError as e:
                    self.add_toast(Adw.Toast(title=_("Failed to save override")))
                    buglog(f"Failed to save keyfile structure to override. Exc: {e}")
                else:
                    self.settings.set_boolean("global-flatpak-theming", True)
                    buglog(f"global-flatpak-theming: {self.settings.get_boolean('global-flatpak-theming')}")
                    #value = global_keyfile.get_string_list("Context", "filesystems")
                    #print(value)
        else:
            self.settings.set_boolean("global-flatpak-theming", False)
            buglog(f"global-flatpak-theming: {self.settings.get_boolean('global-flatpak-theming')}")
