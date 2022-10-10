# css.py
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

import cssutils

COLORS = [
    "blue_",
    "green_",
    "yellow_",
    "orange_",
    "red_",
    "purple_",
    "brown_",
    "light_",
    "dark_",
]


def load_preset_from_css(path):
    css = ""
    variables = {}
    palette = {}

    for color in COLORS:
        palette[color] = {}

    with open(path, "r", encoding="utf-8") as f:
        sheet = cssutils.parseString(f.read())
        for rule in sheet:
            css_text = rule.cssText
            if rule.type == rule.UNKNOWN_RULE:
                if css_text.startswith("@define-color"):
                    name, color = css_text.split(" ", 1)[1].split(" ", 1)
                    for color_name in COLORS:
                        if name.startswith(color_name):
                            palette[name[:-1]][name[-1:]] = color[:-1]
                            break
                    else:
                        variables[name] = color[:-1]
            elif rule.type == rule.STYLE_RULE:
                css += f"\n{rule.cssText}"
    return variables, palette, css
