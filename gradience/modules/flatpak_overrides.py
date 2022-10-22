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


""" Custom exception class """


class InvalidGTKVersion(Exception):
    pass


""" Internal helper functions (shouldn't be used outside this file) """


def get_system_flatpak_path():
    systemPath = GLib.getenv("FLATPAK_SYSTEM_DIR")
    buglog(f"systemPath: {systemPath}")

    if systemPath:
        return systemPath

    systemDataDir = GLib.build_filenamev([GLib.DIR_SEPARATOR_S, "var", "lib"])

    return GLib.build_filenamev([systemDataDir, "flatpak"])


def get_user_flatpak_path():
    userPath = GLib.getenv("FLATPAK_USER_DIR")
    buglog(f"userPath: {userPath}")

    if userPath:
        return userPath

    userDataDir = GLib.build_filenamev([GLib.get_home_dir(), ".local", "share"])

    return GLib.build_filenamev([userDataDir, "flatpak"])


def user_save_keyfile(toast_overlay, settings, user_keyfile, filename, gtk_ver):
    try:
        user_keyfile.save_to_file(filename)
    except GLib.GError as e:
        toast_overlay.add_toast(Adw.Toast(title=_("Failed to save override")))
        buglog(f"Failed to save keyfile structure to override. Exc: {e}")
    else:
        if gtk_ver == "gtk4":
            settings.set_boolean("user-flatpak-theming-gtk4", True)
            buglog(
                f"user-flatpak-theming-gtk4: {settings.get_boolean('user-flatpak-theming-gtk4')}"
            )
        elif gtk_ver == "gtk3":
            settings.set_boolean("user-flatpak-theming-gtk3", True)
            buglog(
                f"user-flatpak-theming-gtk3: {settings.get_boolean('user-flatpak-theming-gtk3')}"
            )


def global_save_keyfile(toast_overlay, settings, global_keyfile, filename, gtk_ver):
    try:
        global_keyfile.save_to_file(filename)
    except GLib.GError as e:
        toast_overlay.add_toast(Adw.Toast(title=_("Failed to save override")))
        buglog(f"Failed to save keyfile structure to override. Exc: {e}")
    else:
        if gtk_ver == "gtk4":
            settings.set_boolean("global-flatpak-theming-gtk4", True)
            buglog(
                f"global-flatpak-theming-gtk4: {settings.get_boolean('global-flatpak-theming-gtk4')}"
            )
        elif gtk_ver == "gtk3":
            settings.set_boolean("global-flatpak-theming-gtk3", True)
            buglog(
                f"global-flatpak-theming-gtk3: {settings.get_boolean('global-flatpak-theming-gtk3')}"
            )


""" Main functions """


def create_gtk_user_override(toast_overlay, settings, gtk_ver):
    override_dir = GLib.build_filenamev([get_user_flatpak_path(), "overrides"])
    buglog(f"override_dir: {override_dir}")

    filename = GLib.build_filenamev([override_dir, "global"])

    user_keyfile = GLib.KeyFile.new()

    is_gtk4 = gtk_ver == "gtk4"
    is_gtk3 = gtk_ver == "gtk3"
    if is_gtk4:
        gtk_path = "xdg-config/gtk-4.0"
    elif is_gtk3:
        gtk_path = "xdg-config/gtk-3.0"
    else:
        raise InvalidGTKVersion(
            f"Invalid GTK version chosen: {gtk_ver}. Please choose between two options: gtk4, gtk3"
        )

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
                    if is_gtk4:
                        settings.set_boolean("user-flatpak-theming-gtk4", False)
                    elif is_gtk3:
                        settings.set_boolean("user-flatpak-theming-gtk3", False)
                    return
                else:
                    buglog("Directories created.")

            file = Gio.File.new_for_path(filename)
            file.create(Gio.FileCreateFlags.NONE, None)

            user_keyfile.load_from_file(filename, GLib.KeyFileFlags.NONE)
            user_keyfile.set_string("Context", "filesystems", gtk_path)

            user_save_keyfile(toast_overlay, settings, user_keyfile, filename, gtk_ver)
        else:
            toast_overlay.add_toast(
                Adw.Toast(title=_("Unexpected file error occurred"))
            )
            buglog(f"Unhandled GLib.FileError error code. Exc: {e}")
    else:
        try:
            filesys_list = user_keyfile.get_string_list("Context", "filesystems")
        except GLib.GError:
            user_keyfile.set_string("Context", "filesystems", gtk_path)
            user_save_keyfile(toast_overlay, settings, user_keyfile, filename, gtk_ver)
        else:
            if gtk_path not in filesys_list:
                user_keyfile.set_string_list(
                    "Context", "filesystems", filesys_list + [gtk_path]
                )
                user_save_keyfile(
                    toast_overlay, settings, user_keyfile, filename, gtk_ver
                )
            else:
                if is_gtk4:
                    settings.set_boolean("user-flatpak-theming-gtk4", True)
                elif is_gtk3:
                    settings.set_boolean("user-flatpak-theming-gtk3", True)
                buglog("Value already exists.")


def remove_gtk_user_override(toast_overlay, settings, gtk_ver):
    override_dir = GLib.build_filenamev([get_user_flatpak_path(), "overrides"])
    buglog(f"override_dir: {override_dir}")

    filename = GLib.build_filenamev([override_dir, "global"])

    user_keyfile = GLib.KeyFile.new()

    is_gtk4 = gtk_ver == "gtk4"
    is_gtk3 = gtk_ver == "gtk3"
    if is_gtk4:
        gtk_path = "xdg-config/gtk-4.0"
    elif is_gtk3:
        gtk_path = "xdg-config/gtk-3.0"
    else:
        raise InvalidGTKVersion(
            f"Invalid GTK version chosen: {gtk_ver}. Please choose between two options: gtk4, gtk3"
        )

    def set_theming():
        if is_gtk4:
            settings.set_boolean("user-flatpak-theming-gtk4", False)
        elif is_gtk3:
            settings.set_boolean("user-flatpak-theming-gtk3", False)

    try:
        user_keyfile.load_from_file(filename, GLib.KeyFileFlags.NONE)
    except GLib.GError as e:
        if e.code == 4:
            set_theming()
            buglog("remove override: File doesn't exist")
        else:
            toast_overlay.add_toast(
                Adw.Toast(title=_("Unexpected file error occurred"))
            )
            buglog(f"Unhandled GLib.FileError error code. Exc: {e}")
    else:
        try:
            filesys_list = user_keyfile.get_string_list("Context", "filesystems")
        except GLib.GError:
            set_theming()
            buglog("remove override: Group/key not found.")
        else:
            if gtk_path in filesys_list:
                buglog(f"before: {filesys_list}")
                filesys_list.remove(gtk_path)
                buglog(f"after: {filesys_list}")

                user_keyfile.set_string_list("Context", "filesystems", filesys_list)
                user_save_keyfile(
                    toast_overlay, settings, user_keyfile, filename, gtk_ver
                )
                buglog("remove override: Value removed.")
            else:
                set_theming()
                buglog("remove override: Value not found.")


""" Do not use this functions for now, as they are lacking authentication"""
# TODO: Implement user authentication using Polkit


def create_gtk_global_override(toast_overlay, settings, gtk_ver):
    override_dir = GLib.build_filenamev([get_system_flatpak_path(), "overrides"])
    buglog(f"override_dir: {override_dir}")

    filename = GLib.build_filenamev([override_dir, "global"])

    global_keyfile = GLib.KeyFile.new()

    is_gtk4 = gtk_ver == "gtk4"
    is_gtk3 = gtk_ver == "gtk3"
    if is_gtk4:
        gtk_path = "xdg-config/gtk-4.0"
    elif is_gtk3:
        gtk_path = "xdg-config/gtk-3.0"
    else:
        raise InvalidGTKVersion(
            f"Invalid GTK version chosen: {gtk_ver}. Please choose between two options: gtk4, gtk3"
        )

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
                    if is_gtk4:
                        settings.set_boolean("global-flatpak-theming-gtk4", False)
                    elif is_gtk3:
                        settings.set_boolean("global-flatpak-theming-gtk3", False)
                    return
                else:
                    buglog("Directories created.")

            file = Gio.File.new_for_path(filename)
            file.create(Gio.FileCreateFlags.NONE, None)

            global_keyfile.load_from_file(filename, GLib.KeyFileFlags.NONE)
            global_keyfile.set_string("Context", "filesystems", gtk_path)

            global_save_keyfile(
                toast_overlay, settings, global_keyfile, filename, gtk_ver
            )
        else:
            toast_overlay.add_toast(
                Adw.Toast(title=_("Unexpected file error occurred"))
            )
            buglog(f"Unhandled GLib.FileError error code. Exc: {e}")
    else:
        try:
            filesys_list = global_keyfile.get_string_list("Context", "filesystems")
        except GLib.GError:
            global_keyfile.set_string("Context", "filesystems", gtk_path)
            global_save_keyfile(
                toast_overlay, settings, global_keyfile, filename, gtk_ver
            )
        else:
            if gtk_path not in filesys_list:
                global_keyfile.set_string_list(
                    "Context", "filesystems", filesys_list + [gtk_path]
                )
                global_save_keyfile(
                    toast_overlay, settings, global_keyfile, filename, gtk_ver
                )
            else:
                if is_gtk4:
                    settings.set_boolean("global-flatpak-theming-gtk4", True)
                elif is_gtk3:
                    settings.set_boolean("global-flatpak-theming-gtk3", True)
                buglog("Value already exists.")


def remove_gtk_global_override(toast_overlay, settings, gtk_ver):
    override_dir = GLib.build_filenamev([get_system_flatpak_path(), "overrides"])
    buglog(f"override_dir: {override_dir}")

    filename = GLib.build_filenamev([override_dir, "global"])

    global_keyfile = GLib.KeyFile.new()

    is_gtk4 = gtk_ver == "gtk4"
    is_gtk3 = gtk_ver == "gtk3"
    if is_gtk4:
        gtk_path = "xdg-config/gtk-4.0"
    elif is_gtk3:
        gtk_path = "xdg-config/gtk-3.0"
    else:
        raise InvalidGTKVersion(
            f"Invalid GTK version chosen: {gtk_ver}. Please choose between two options: gtk4, gtk3"
        )

    def set_theming():
        if is_gtk4:
            settings.set_boolean("user-flatpak-theming-gtk4", False)
        elif is_gtk3:
            settings.set_boolean("user-flatpak-theming-gtk3", False)

    try:
        global_keyfile.load_from_file(filename, GLib.KeyFileFlags.NONE)
    except GLib.GError as e:
        if e.code == 4:
            set_theming()
            buglog("remove override: File doesn't exist")
        else:
            toast_overlay.add_toast(
                Adw.Toast(title=_("Unexpected file error occurred"))
            )
            buglog(f"Unhandled GLib.FileError error code. Exc: {e}")
    else:
        try:
            filesys_list = global_keyfile.get_string_list("Context", "filesystems")
        except GLib.GError:
            set_theming()
            buglog("remove override: Group/key not found.")
        else:
            if gtk_path in filesys_list:
                buglog(f"before: {filesys_list}")
                filesys_list.remove(gtk_path)
                buglog(f"after: {filesys_list}")

                global_keyfile.set_string_list("Context", "filesystems", filesys_list)
                global_save_keyfile(
                    toast_overlay, settings, global_keyfile, filename, gtk_ver
                )
                buglog("remove override: Value removed.")
            else:
                set_theming()
                buglog("remove override: Value not found.")
