# colors.py
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

import material_color_utilities_python as monet


def rgba_from_argb(argb, alpha=None) -> str:
    base = "rgba({}, {}, {}, {})"

    red = monet.redFromArgb(argb)
    green = monet.greenFromArgb(argb)
    blue = monet.blueFromArgb(argb)
    if not alpha:
        alpha = monet.alphaFromArgb(argb)

    return base.format(red, green, blue, alpha)
