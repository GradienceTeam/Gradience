# common.py
#
# Change the look of Adwaita, with ease
# Copyright (C) 2022-2023, Gradience Team
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

import re
import os

from anyascii import anyascii

from gi.repository import Gio


def to_slug_case(non_slug) -> str:
    return re.sub(r"[^0-9a-z]+", "-", anyascii(non_slug).lower()).strip("-")

def extract_version(text, prefix_text=None):
    '''
    Extracts version number from a provided text.

    You can also set the prefix_text parameter to reduce searching to
    lines with only this text prefixed to the version number.
    '''
    if not prefix_text:
        version = re.search(r"\s*([0-9.]+)", text)
    else:
        version = re.search(prefix_text + r"\s*([0-9.]+)", text)

    return version.__getitem__(1)

def run_command(
    command: list,
    stdout_pipe=False,
    get_stdout_text=False,
    allow_escaping:bool = False) -> (Gio.Subprocess, Gio.UnixInputStream, str):
    '''
    Spawns a new child process (subprocess) using Gio's Subprocess class.

    To retrieve process stdout pipe, enable `stdout_pipe` parameter.

    To retrieve stdout in a text form, enable `get_stdout_text` parameter.

    You can enable executing commands outside Flatpak sandbox by enabling
    `allow_escaping` parameter.
    '''
    if allow_escaping and os.environ.get('FLATPAK_ID'):
        command = ['flatpak-spawn', '--host'] + command

    if stdout_pipe or get_stdout_text:
        flags = Gio.SubprocessFlags.STDOUT_PIPE
    else:
        flags = Gio.SubprocessFlags.NONE

    gsubprocess = Gio.Subprocess.new(command, flags)
    stdout_stream = gsubprocess.get_stdout_pipe()

    if stdout_pipe:
        return stdout_stream

    if get_stdout_text:
        data_stream = Gio.DataInputStream.new(stdout_stream)

        stdout_bytes = data_stream.read_line(cancellable=None)
        stdout = stdout_bytes[0].decode()

        return stdout

    return gsubprocess
