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
import subprocess

from anyascii import anyascii


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

def run_command(command, *args, **kwargs):
    if isinstance(command, str): # run on the host
        command = [command]
    if os.environ.get('FLATPAK_ID'): # run in flatpak
        command = ['flatpak-spawn', '--host'] + command

    return subprocess.run(command, *args, **kwargs, check=True)
