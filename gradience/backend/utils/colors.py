# colors.py
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

import material_color_utilities_python as monet

from gradience.backend.globals import adw_variables_prefixes, adw_palette_prefixes

from gradience.backend.logger import Logger

logging = Logger(logger_name="ColorUtils")


def rgb_to_hash(rgb) -> [str, float]:
    """
    This function converts rgb or rgba-formatted color code to an hexadecimal code.

    Alpha channel from RGBA color codes is passed without any conversion
    as a second return variable and is completely ignored in hexadecimal codes
    to remain compliant with web stantards.
    """
    if rgb.startswith("rgb"):
        rgb_values = rgb.strip("rgb()")

    if rgb.startswith("rgba"):
        rgb_values = rgb.strip("rgba()")

    rgb_list = rgb_values.split(",")

    red = int(rgb_list[0])
    green = int(rgb_list[1])
    blue = int(rgb_list[2])
    alpha = None

    if len(rgb_list) == 4:
        alpha = float(rgb_list[3])

    hex_out = [f"{red:x}", f"{green:x}", f"{blue:x}"]

    for i, hex_part in enumerate(hex_out):
        if len(hex_part) == 1:
            hex_out[i] = "0" + hex_part

    return "#" + "".join(hex_out), alpha

def argb_to_color_code(argb, alpha=None) -> str:
    """
    This function can return either an hexadecimal or rgba-formatted color code.

    By default this function returns hexadecimal color codes.
    If alpha parameter is specified, then the function will return
    an rgba-formatted color code.
    """
    rgba_base = "rgba({0}, {1}, {2}, {3})"

    red = monet.redFromArgb(argb)
    green = monet.greenFromArgb(argb)
    blue = monet.blueFromArgb(argb)
    if not alpha:
        alpha = monet.alphaFromArgb(argb)

    if alpha in (255, 0.0):
        return monet.hexFromArgb(argb)

    return rgba_base.format(red, green, blue, alpha)

def color_vars_to_color_code(variables: dict, palette: dict):
    """
    This function converts GTK color variables to color code
    (hexadecimal code if no transparency channel, RGBA format if otherwise).

    You can bypass passing a `palette` parameter if you put an None value to it.
    This isn't recommended however, because in most cases you'll be unable to determine
    if variables you pass don't contain any palette color variables.
    """
    if palette == None:
        logging.warning("Palette parameter in `color_vars_to_color_code()` function not set. Incoming bugs ahead!")

    def __has_palette_prefix(color):
        return any(prefix in color for prefix in adw_palette_prefixes)

    def __has_variable_prefix(color):
        return any(prefix in color for prefix in adw_variables_prefixes)

    def __update_vars(var_type, variable, color_value):
        if var_type == "palette":
            variables[variable] = palette[color_value[:-1]][color_value[-1:]]
        elif var_type == "variable":
            variables[variable] = variables[color_value]

        if __has_variable_prefix(variables[variable]):
            __update_variable_vars(variable, variables[variable])

        if __has_palette_prefix(variables[variable]):
            __update_palette_vars(variable, variables[variable])

    for variable, color in variables.items():
        color_value = color[1:] # Remove '@' from the beginning of the color variable

        if __has_palette_prefix(color_value) and palette != None:
            __update_vars("palette", variable, color_value)

        if __has_variable_prefix(color_value):
            __update_vars("variable", variable, color_value)
