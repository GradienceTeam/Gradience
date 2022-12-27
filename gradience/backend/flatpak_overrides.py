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

from gradience.backend.constants import app_id

from gradience.backend.logger import Logger

logging = Logger()


""" Custom exception class """


class InvalidGTKVersion(Exception):
    pass


""" Internal helper functions (shouldn't be used outside this module) """


def __get_system_flatpak_path():
    systemPath = GLib.getenv("FLATPAK_SYSTEM_DIR")
    logging.debug(f"systemPath: {systemPath}")

    if systemPath:
        return systemPath

    systemDataDir = GLib.build_filenamev([GLib.DIR_SEPARATOR_S, "var", "lib"])

    return GLib.build_filenamev([systemDataDir, "flatpak"])


def __get_user_flatpak_path():
    userPath = GLib.getenv("FLATPAK_USER_DIR")
    logging.debug(f"userPath: {userPath}")

    if userPath:
        return userPath

    userDataDir = GLib.build_filenamev(
        [GLib.get_home_dir(), ".local", "share"])

    return GLib.build_filenamev([userDataDir, "flatpak"])


def __user_save_keyfile(user_keyfile, filename, settings=None, gtk_ver=None, toast_overlay=None):
    try:
        user_keyfile.save_to_file(filename)
    except GLib.GError as e:
        logging.error("Failed to save keyfile structure to override.", exc=e)
        if toast_overlay:
            toast_overlay.add_toast(Adw.Toast(title=_("Failed to save override")))
    else:
        if gtk_ver == "gtk4" and settings:
            settings.set_boolean("user-flatpak-theming-gtk4", True)
            logging.debug(
                f"user-flatpak-theming-gtk4: {settings.get_boolean('user-flatpak-theming-gtk4')}"
            )
        elif gtk_ver == "gtk3" and settings:
            settings.set_boolean("user-flatpak-theming-gtk3", True)
            logging.debug(
                f"user-flatpak-theming-gtk3: {settings.get_boolean('user-flatpak-theming-gtk3')}"
            )
        elif not gtk_ver and not settings:
            logging.debug("DEV WARNING: 'gtk_ver' and 'settings' parameters aren't set for '__user_save_keyfile' function. Unless you aren't using '{create,remove}_*_override' functions, this is a bug.")


def __global_save_keyfile(global_keyfile, filename, settings=None, gtk_ver=None, toast_overlay=None):
    try:
        global_keyfile.save_to_file(filename)
    except GLib.GError as e:
        logging.error("Failed to save keyfile structure to override.", exc=e)
        if toast_overlay:
            toast_overlay.add_toast(Adw.Toast(title=_("Failed to save override")))
    else:
        if gtk_ver == "gtk4" and settings:
            settings.set_boolean("global-flatpak-theming-gtk4", True)
            logging.debug(
                f"global-flatpak-theming-gtk4: {settings.get_boolean('global-flatpak-theming-gtk4')}"
            )
        elif gtk_ver == "gtk3" and settings:
            settings.set_boolean("global-flatpak-theming-gtk3", True)
            logging.debug(
                f"global-flatpak-theming-gtk3: {settings.get_boolean('global-flatpak-theming-gtk3')}"
            )
        elif not gtk_ver and not settings:
            logging.debug("DEV WARNING: 'gtk_ver' and 'settings' parameters aren't set for '__global_save_keyfile' function. Unless you aren't using '{create,remove}_*_override' functions, this is a bug.")


""" Main functions """


def list_file_access():
    override_dir = GLib.build_filenamev([__get_user_flatpak_path(), "overrides"])
    logging.debug(f"override_dir: {override_dir}")

    filename = GLib.build_filenamev([override_dir, app_id])

    user_keyfile = GLib.KeyFile.new()

    try:
        user_keyfile.load_from_file(filename, GLib.KeyFileFlags.NONE)
    except GLib.GError as e:
        if e.code == 4:
            logging.debug("Gradience overrides file doesn't exist")
            return False
        else:
            logging.error("Unhandled GLib.FileError error code.", exc=e)
            raise
    else:
        try:
            filesys_list = user_keyfile.get_string_list(
                "Context", "filesystems")
        except GLib.GError:
            logging.debug("No values in 'filesystems' override")
            return False
        else:
            return filesys_list


# TODO: Frontend: Show information to user to relaunch Gradience, as this function modifies \
# Gradience's overrides.
def allow_file_access(directory, toast_overlay=None):
    override_dir = GLib.build_filenamev([__get_user_flatpak_path(), "overrides"])
    logging.debug(f"override_dir: {override_dir}")

    without_access_spec = (
        not ":ro" in directory
        and not ":rw" in directory
        and not ":create" in directory
    )

    if without_access_spec:
        directory += ":ro"

    filename = GLib.build_filenamev([override_dir, app_id])

    user_keyfile = GLib.KeyFile.new()

    try:
        user_keyfile.load_from_file(filename, GLib.KeyFileFlags.NONE)
    except GLib.GError as e:
        if e.code == 4:
            logging.debug("File doesn't exist. Attempting to create one")
            if not os.path.exists(override_dir):
                try:
                    dirs = Gio.File.new_for_path(override_dir)
                    dirs.make_directory_with_parents(None)
                except GLib.GError as e:
                    logging.error("Unable to create directories.", exc=e)
                    raise
                else:
                    logging.debug("Directories created.")

            file = Gio.File.new_for_path(filename)
            file.create(Gio.FileCreateFlags.NONE, None)

            user_keyfile.load_from_file(filename, GLib.KeyFileFlags.NONE)
            user_keyfile.set_string("Context", "filesystems", directory)

            __user_save_keyfile(user_keyfile, filename,
                                toast_overlay=toast_overlay)
        else:
            logging.error("Unhandled GLib.FileError error code.", exc=e)
            if toast_overlay:
                toast_overlay.add_toast(
                    Adw.Toast(title=_("Unexpected file error occurred"))
                )
            raise
    else:
        try:
            filesys_list = user_keyfile.get_string_list(
                "Context", "filesystems")
        except GLib.GError:
            user_keyfile.set_string("Context", "filesystems", directory)
            __user_save_keyfile(user_keyfile, filename,
                                toast_overlay=toast_overlay)
        else:
            if directory not in filesys_list:
                user_keyfile.set_string_list(
                    "Context", "filesystems", filesys_list + [directory]
                )
                __user_save_keyfile(user_keyfile, filename,
                                    toast_overlay=toast_overlay)
            else:
                logging.info("Path is already allowed")


# TODO: Frontend: Show information to user to relaunch Gradience, as this function modifies \
# Gradience's overrides.
def disallow_file_access(directory, toast_overlay=None):
    override_dir = GLib.build_filenamev([__get_user_flatpak_path(), "overrides"])
    logging.debug(f"override_dir: {override_dir}")

    filename = GLib.build_filenamev([override_dir, app_id])

    user_keyfile = GLib.KeyFile.new()

    try:
        user_keyfile.load_from_file(filename, GLib.KeyFileFlags.NONE)
    except GLib.GError as e:
        if e.code == 4:
            logging.debug("File doesn't exist")
            return
        else:
            logging.error("Unhandled GLib.FileError error code.", exc=e)
            if toast_overlay:
                toast_overlay.add_toast(
                    Adw.Toast(title=_("Unexpected file error occurred"))
                )
            raise
    else:
        try:
            filesys_list = user_keyfile.get_string_list(
                "Context", "filesystems")
        except GLib.GError:
            logging.debug("Group/key not found")
            return
        else:
            if directory in filesys_list:
                logging.debug(f"before: {filesys_list}")
                filesys_list.remove(directory)
                logging.debug(f"after: {filesys_list}")

                user_keyfile.set_string_list(
                    "Context", "filesystems", filesys_list)
                __user_save_keyfile(user_keyfile, filename,
                                    toast_overlay=toast_overlay)
                logging.debug("Path removed")
            else:
                logging.debug("Path doesn't exist in overrides")
                return


def create_gtk_user_override(settings, gtk_ver, toast_overlay=None):
    override_dir = GLib.build_filenamev([__get_user_flatpak_path(), "overrides"])
    logging.debug(f"override_dir: {override_dir}")

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
            logging.debug("File doesn't exist. Attempting to create one")
            if not os.path.exists(override_dir):
                try:
                    dirs = Gio.File.new_for_path(override_dir)
                    dirs.make_directory_with_parents(None)
                except GLib.GError as e:
                    logging.error("Unable to create directories.", exc=e)
                    if is_gtk4:
                        settings.set_boolean(
                            "user-flatpak-theming-gtk4", False)
                    elif is_gtk3:
                        settings.set_boolean(
                            "user-flatpak-theming-gtk3", False)
                    return
                else:
                    logging.debug("Directories created.")

            file = Gio.File.new_for_path(filename)
            file.create(Gio.FileCreateFlags.NONE, None)

            user_keyfile.load_from_file(filename, GLib.KeyFileFlags.NONE)
            user_keyfile.set_string("Context", "filesystems", gtk_path)

            __user_save_keyfile(user_keyfile, filename,
                                settings, gtk_ver, toast_overlay)
        else:
            logging.error("Unhandled GLib.FileError error code.", exc=e)
            if toast_overlay:
                toast_overlay.add_toast(
                    Adw.Toast(title=_("Unexpected file error occurred"))
                )
    else:
        try:
            filesys_list = user_keyfile.get_string_list(
                "Context", "filesystems")
        except GLib.GError:
            user_keyfile.set_string("Context", "filesystems", gtk_path)
            __user_save_keyfile(user_keyfile, filename,
                                settings, gtk_ver, toast_overlay)
        else:
            if gtk_path not in filesys_list:
                user_keyfile.set_string_list(
                    "Context", "filesystems", filesys_list + [gtk_path]
                )
                __user_save_keyfile(user_keyfile, filename,
                                    settings, gtk_ver, toast_overlay)
            else:
                if is_gtk4:
                    settings.set_boolean("user-flatpak-theming-gtk4", True)
                elif is_gtk3:
                    settings.set_boolean("user-flatpak-theming-gtk3", True)
                logging.debug("Value already exists.")


def remove_gtk_user_override(settings, gtk_ver, toast_overlay=None):
    override_dir = GLib.build_filenamev([__get_user_flatpak_path(), "overrides"])
    logging.debug(f"override_dir: {override_dir}")

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
            logging.warning("remove override: File doesn't exist")
        else:
            logging.error("Unhandled GLib.FileError error code.", exc=e)
            if toast_overlay:
                toast_overlay.add_toast(
                    Adw.Toast(title=_("Unexpected file error occurred"))
                )
    else:
        try:
            filesys_list = user_keyfile.get_string_list(
                "Context", "filesystems")
        except GLib.GError:
            set_theming()
            logging.warning("remove override: Group/key not found.")
        else:
            if gtk_path in filesys_list:
                logging.debug(f"before: {filesys_list}")
                filesys_list.remove(gtk_path)
                logging.debug(f"after: {filesys_list}")

                user_keyfile.set_string_list(
                    "Context", "filesystems", filesys_list)
                __user_save_keyfile(user_keyfile, filename,
                                    settings, gtk_ver, toast_overlay)
                logging.debug("remove override: Value removed.")
            else:
                set_theming()
                logging.debug("remove override: Value not found.")


""" Do not use this functions for now, as they are lacking authentication"""
# TODO: Implement user authentication using Polkit


def create_gtk_global_override(settings, gtk_ver, toast_overlay=None):
    override_dir = GLib.build_filenamev(
        [__get_system_flatpak_path(), "overrides"])
    logging.debug(f"override_dir: {override_dir}")

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
            logging.debug("File doesn't exist. Attempting to create one")
            if not os.path.exists(override_dir):
                try:
                    dirs = Gio.File.new_for_path(override_dir)
                    dirs.make_directory_with_parents(None)
                except GLib.GError as e:
                    logging.error("Unable to create directories.", exc=e)
                    if is_gtk4:
                        settings.set_boolean(
                            "global-flatpak-theming-gtk4", False)
                    elif is_gtk3:
                        settings.set_boolean(
                            "global-flatpak-theming-gtk3", False)
                    return
                else:
                    logging.debug("Directories created.")

            file = Gio.File.new_for_path(filename)
            file.create(Gio.FileCreateFlags.NONE, None)

            global_keyfile.load_from_file(filename, GLib.KeyFileFlags.NONE)
            global_keyfile.set_string("Context", "filesystems", gtk_path)

            __global_save_keyfile(global_keyfile, filename,
                                    settings, gtk_ver, toast_overlay)
        else:
            logging.error("Unhandled GLib.FileError error code.", exc=e)
            if toast_overlay:
                toast_overlay.add_toast(
                    Adw.Toast(title=_("Unexpected file error occurred"))
                )
    else:
        try:
            filesys_list = global_keyfile.get_string_list(
                "Context", "filesystems")
        except GLib.GError:
            global_keyfile.set_string("Context", "filesystems", gtk_path)
            __global_save_keyfile(global_keyfile, filename,
                                    settings, gtk_ver, toast_overlay)
        else:
            if gtk_path not in filesys_list:
                global_keyfile.set_string_list(
                    "Context", "filesystems", filesys_list + [gtk_path]
                )
                __global_save_keyfile(global_keyfile, filename,
                                        settings, gtk_ver, toast_overlay)
            else:
                if is_gtk4:
                    settings.set_boolean("global-flatpak-theming-gtk4", True)
                elif is_gtk3:
                    settings.set_boolean("global-flatpak-theming-gtk3", True)
                logging.debug("Value already exists.")


def remove_gtk_global_override(settings, gtk_ver, toast_overlay=None):
    override_dir = GLib.build_filenamev(
        [__get_system_flatpak_path(), "overrides"])
    logging.debug(f"override_dir: {override_dir}")

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
            logging.warning("remove override: File doesn't exist")
        else:
            logging.error("Unhandled GLib.FileError error code.", exc=e)
            if toast_overlay:
                toast_overlay.add_toast(
                    Adw.Toast(title=_("Unexpected file error occurred"))
                )
    else:
        try:
            filesys_list = global_keyfile.get_string_list(
                "Context", "filesystems")
        except GLib.GError:
            set_theming()
            logging.warning("remove override: Group/key not found.")
        else:
            if gtk_path in filesys_list:
                logging.debug(f"before: {filesys_list}")
                filesys_list.remove(gtk_path)
                logging.debug(f"after: {filesys_list}")

                global_keyfile.set_string_list(
                    "Context", "filesystems", filesys_list)
                __global_save_keyfile(global_keyfile, filename,
                                        settings, gtk_ver, toast_overlay)
                logging.debug("remove override: Value removed.")
            else:
                set_theming()
                logging.debug("remove override: Value not found.")
