# flatpak_overrides.py
#
# Change the look of Adwaita, with ease
# Copyright (C) 2022 Gradience Team
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

from gi.repository import GLib, Gio, Adw

from .utils import buglog


''' Internal helper functions (shouldn't be used outside this file) '''
def get_system_flatpak_path():
    systemPath = GLib.getenv("FLATPAK_SYSTEM_DIR")
    buglog(f"systemPath: {systemPath}")
    
    if systemPath:
        return systemPath

    systemDataDir = GLib.build_filenamev([
        GLib.DIR_SEPARATOR_S, "var", "lib"
    ])

    return GLib.build_filenamev([systemDataDir, "flatpak"])

def get_user_flatpak_path():
    userPath = GLib.getenv("FLATPAK_USER_DIR")
    buglog(f"userPath: {userPath}")
    
    if userPath:
        return userPath

    userDataDir = GLib.build_filenamev([
        GLib.get_home_dir(), ".local", "share"
    ])

    return GLib.build_filenamev([userDataDir, "flatpak"])

def user_save_keyfile(toast_overlay, settings, user_keyfile, filename):
    try:
        user_keyfile.save_to_file(filename)
    except Glib.GError as e:
        toast_overlay.add_toast(Adw.Toast(title=_("Failed to save override")))
        buglog(f"Failed to save keyfile structure to override. Exc: {e}")
    else:
        settings.set_boolean("user-flatpak-theming", True)
        buglog(f"user-flatpak-theming: {settings.get_boolean('user-flatpak-theming')}")

def global_save_keyfile(toast_overlay, settings, global_keyfile, filename):
    try:
        global_keyfile.save_to_file(filename)
    except Glib.GError as e:
        toast_overlay.add_toast(Adw.Toast(title=_("Failed to save override")))
        buglog(f"Failed to save keyfile structure to override. Exc: {e}")
    else:
        settings.set_boolean("global-flatpak-theming", True)
        buglog(f"global-flatpak-theming: {settings.get_boolean('global-flatpak-theming')}")


''' Main functions '''
def create_gtk4_user_override(toast_overlay, settings):
    override_dir = GLib.build_filenamev([
        get_user_flatpak_path(), "overrides"
    ])
    print(f"override_dir: {override_dir}")

    filename = GLib.build_filenamev([
        override_dir, "global"
    ])

    user_keyfile = GLib.KeyFile.new()

    try:
        user_keyfile.load_from_file(filename, GLib.KeyFileFlags.NONE)
    except GLib.GError as e:
        if e.code == 4:
            buglog("File doesn't exist. Attempting to create one")
            if not os.path.exists(override_dir):
                try:
                    dirs = Gio.File.new_for_path(override_dir)
                    dirs.make_directory_with_parents(None)
                except GLib.GError as e:
                    buglog(f"Unable to create directories. Exc: {e}")
                else:
                    buglog("Directories created.")

            file = Gio.File.new_for_path(filename)
            file.create(Gio.FileCreateFlags.NONE, None)

            user_keyfile.load_from_file(filename, GLib.KeyFileFlags.NONE)
            user_keyfile.set_string("Context", "filesystems", "xdg-config/gtk-4.0") 

            user_save_keyfile(toast_overlay, settings, user_keyfile, filename)
        else:
            toast_overlay.add_toast(Adw.Toast(title=_("Unexpected file error occurred")))
            buglog(f"Unhandled GLib.FileError error code. Exc: {e}")
    else:
        try:
            filesys_list = user_keyfile.get_string_list("Context", "filesystems")
        except GLib.GError:
            user_keyfile.set_string("Context", "filesystems", "xdg-config/gtk-4.0")
            user_save_keyfile(toast_overlay, settings, user_keyfile, filename)
        else:
            if not "xdg-config/gtk-4.0" in filesys_list:
                user_keyfile.set_string_list("Context", "filesystems", filesys_list + ["xdg-config/gtk-4.0"])
                user_save_keyfile(toast_overlay, settings, user_keyfile, filename)
            else:
                settings.set_boolean("user-flatpak-theming", True)
                buglog("Value already exists.")

def remove_gtk4_user_override(toast_overlay, settings):
    override_dir = GLib.build_filenamev([
        get_user_flatpak_path(), "overrides"
    ])
    print(f"override_dir: {override_dir}")

    filename = GLib.build_filenamev([
        override_dir, "global"
    ])

    user_keyfile = GLib.KeyFile.new()

    try:
        user_keyfile.load_from_file(filename, GLib.KeyFileFlags.NONE)
    except GLib.GError as e:
        if e.code == 4:
            settings.set_boolean("user-flatpak-theming", False)
            buglog("remove override: File doesn't exist")
        else:
            toast_overlay.add_toast(Adw.Toast(title=_("Unexpected file error occurred")))
            buglog(f"Unhandled GLib.FileError error code. Exc: {e}")
    else:
        try:
            filesys_list = user_keyfile.get_string_list("Context", "filesystems")
        except GLib.GError:
            settings.set_boolean("user-flatpak-theming", False)
            buglog("remove override: Group/key not found.")
        else:
            if "xdg-config/gtk-4.0" in filesys_list:
                buglog(f"before: {filesys_list}")
                filesys_list.remove("xdg-config/gtk-4.0")
                buglog(f"after: {filesys_list}")

                user_keyfile.set_string_list("Context", "filesystems", filesys_list)
                user_save_keyfile(toast_overlay, settings, user_keyfile, filename)
                buglog("remove override: Value removed.")
            else:
                settings.set_boolean("user-flatpak-theming", False)
                buglog("remove override: Value not found.")

''' Do not use this functions for now, as they are lacking authentication'''
# TODO: Implement user authentication using Polkit
def create_gtk4_global_override(toast_overlay, settings):
    override_dir = GLib.build_filenamev([
        get_system_flatpak_path(), "overrides"
    ])
    print(f"override_dir: {override_dir}")

    filename = GLib.build_filenamev([
        self.get_system_flatpak_path(), "global"
    ])

    global_keyfile = GLib.KeyFile.new()

    try:
        global_keyfile.load_from_file(filename, GLib.KeyFileFlags.NONE)
    except GLib.GError as e:
        if e.code == 4:
            buglog("File doesn't exist. Attempting to create one")
            if not os.path.exists(override_dir):
                try:
                    dirs = Gio.File.new_for_path(override_dir)
                    dirs.make_directory_with_parents(None)
                except GLib.GError as e:
                    buglog(f"Unable to create directories. Exc: {e}")
                else:
                    buglog("Directories created.")

            file = Gio.File.new_for_path(filename)
            file.create(Gio.FileCreateFlags.NONE, None)

            global_keyfile.load_from_file(filename, GLib.KeyFileFlags.NONE)
            global_keyfile.set_string("Context", "filesystems", "xdg-config/gtk-4.0") 

            global_save_keyfile(toast_overlay, settings, global_keyfile, filename)
        else:
            toast_overlay.add_toast(Adw.Toast(title=_("Unexpected file error occurred")))
            buglog(f"Unhandled GLib.FileError error code. Exc: {e}")
    else:
        try:
            filesys_list = global_keyfile.get_string_list("Context", "filesystems")
        except GLib.GError:
            global_keyfile.set_string("Context", "filesystems", "xdg-config/gtk-4.0")
            global_save_keyfile(toast_overlay, settings, global_keyfile, filename)
        else:
            if not "xdg-config/gtk-4.0" in filesys_list:
                global_keyfile.set_string_list("Context", "filesystems", filesys_list + ["xdg-config/gtk-4.0"])
                global_save_keyfile(toast_overlay, settings, global_keyfile, filename)
            else:
                settings.set_boolean("global-flatpak-theming", True)
                buglog("Value already exists.")

def remove_gtk4_global_override(toast_overlay, settings):
    override_dir = GLib.build_filenamev([
        get_system_flatpak_path(), "overrides"
    ])
    print(f"override_dir: {override_dir}")
    
    filename = GLib.build_filenamev([
        self.get_system_flatpak_path(), "global"
    ])

    global_keyfile = GLib.KeyFile.new()

    try:
        global_keyfile.load_from_file(filename, GLib.KeyFileFlags.NONE)
    except GLib.GError as e:
        if e.code == 4:
            settings.set_boolean("global-flatpak-theming", False)
            buglog("remove override: File doesn't exist")
        else:
            toast_overlay.add_toast(Adw.Toast(title=_("Unexpected file error occurred")))
            buglog(f"Unhandled GLib.FileError error code. Exc: {e}")
    else:
        try:
            filesys_list = global_keyfile.get_string_list("Context", "filesystems")
        except GLib.GError:
            settings.set_boolean("global-flatpak-theming", False)
            buglog("remove override: Group/key not found.")
        else:
            if "xdg-config/gtk-4.0" in filesys_list:
                buglog(f"before: {filesys_list}")
                filesys_list.remove("xdg-config/gtk-4.0")
                buglog(f"after: {filesys_list}")

                global_keyfile.set_string_list("Context", "filesystems", filesys_list)
                global_save_keyfile(toast_overlay, settings, global_keyfile, filename)
                buglog("remove override: Value removed.")
            else:
                settings.set_boolean("global-flatpak-theming", False)
                buglog("remove override: Value not found.")