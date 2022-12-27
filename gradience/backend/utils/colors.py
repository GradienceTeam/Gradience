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

def argb_to_color_code(argb, alpha=None) -> str:
    """
    This function can return either an hexadecimal or rgba-formatted color code.

    By default this function returns hexadecimal color codes.
    If alpha parameter is specified, then the function will return
    an rgba-formatted color code.
    """
    hex_base = "#{0:x}{1:x}{2:x}"
    rgba_base = "rgba({0}, {1}, {2}, {3})"

    red_chnl = monet.redFromArgb(argb)
    green_chnl = monet.greenFromArgb(argb)
    blue_chnl = monet.blueFromArgb(argb)
    alpha_chnl = alpha

    if not alpha:
        alpha_chnl = monet.alphaFromArgb(argb)

    if alpha_chnl in (255, 0.0):
        return hex_base.format(red_chnl, green_chnl, blue_chnl)

    return rgba_base.format(red_chnl, green_chnl, blue_chnl, alpha_chnl)
