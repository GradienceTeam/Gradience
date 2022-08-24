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

from anyascii import anyascii
from gradience.constants import build_type


def to_slug_case(non_slug):
    return re.sub(r"[^0-9a-z]+", "-", anyascii(non_slug).lower()).strip("-")

# Use it instead of print(), so there isn't any output in stdout if Gradience was build in release mode
# TODO: Can be replaced with `logging` module [https://docs.python.org/3/library/logging.html] in future
def buglog(*args):
    if build_type == "debug":
        message = ""
        for obj in args:
            message += str(obj)
        return print(f"[DEBUG]: {message}")
