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

import os

from jinja2 import Environment, FileSystemLoader


def modify_colors(scss_path, output_path, **vars):
    env = Environment(
        loader=FileSystemLoader(os.path.dirname(scss_path)),
    )
    template = env.get_template("_colors.txt")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(template.render(**vars))
