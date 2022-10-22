# utils.py
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

import re
import logging
import os

from subprocess import run
from anyascii import anyascii
from gradience.constants import build_type


if build_type == "debug":
    logging.basicConfig(
        level=logging.DEBUG, format="[%(levelname)s] [%(name)s] %(message)s"
    )
else:
    logging.basicConfig(
        level=logging.WARNING, format="[%(levelname)s] [%(name)s] %(message)s"
    )


def to_slug_case(non_slug):
    return re.sub(r"[^0-9a-z]+", "-", anyascii(non_slug).lower()).strip("-")


# Use it instead of print(), so there isn't any output in stdout if
# Gradience is build in release mode
def buglog(*args):
    logging.debug(*args)


def run_command(command, *args, **kwargs):

    if isinstance(command, str):  # run on the host
        command = [command]
    if os.environ.get("FLATPAK_ID"):  # run in flatpak
        command = ["flatpak-spawn", "--host"] + command

    return run(command, *args, **kwargs)
