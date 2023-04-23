# css_parser.py
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

from gradience.backend.globals import adw_palette_prefixes


# Regular expressions
define_color = re.compile(r"(@define-color .*[^\s])")
not_define_color = re.compile(r"(^(?:(?!@define-color).)*$)")

def parse_css(path):
    css = ""
    variables = {}
    palette = {}

    for color in adw_palette_prefixes:
        palette[color] = {}

    with open(path, "r", encoding="utf-8") as sheet:
        for line in sheet:
            cdefine_match = re.search(define_color, line)
            not_cdefine_match = re.search(not_define_color, line)
            if cdefine_match != None: # If @define-color variable declarations were found
                palette_part = cdefine_match.__getitem__(1) # Get the second item of the re.Match object
                name, color = palette_part.split(" ", 1)[1].split(" ", 1)
                if name.startswith(tuple(adw_palette_prefixes)): # Palette colors
                    palette[name[:-1]][name[-1:]] = color[:-1]
                else: # Other color variables
                    variables[name] = color[:-1]
            elif not_cdefine_match != None: # If CSS rules were found
                css_part = not_cdefine_match.__getitem__(1)
                css += f"{css_part}\n"

        sheet.close()
        return variables, palette, css
