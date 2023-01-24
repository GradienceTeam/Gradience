# shell.py
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

from gi.repository import Gio

from gradience.backend.utils.common import extract_version


# TODO: Make it Flatpak-friendly (maybe move most of the code to run_command function?)
def get_shell_version():
    result = Gio.Subprocess.new(["gnome-shell", "--version"], Gio.SubprocessFlags.STDOUT_PIPE)

    stdout_stream = result.get_stdout_pipe()
    stdout_bytes = stdout_stream.read_bytes(count=20, cancellable=None).get_data() #count = number of bytes to read, "test" = 4 bytes
    stdout = stdout_bytes.decode().replace("\n", "")

    shell_version = extract_version(stdout, "GNOME Shell")

    return shell_version
