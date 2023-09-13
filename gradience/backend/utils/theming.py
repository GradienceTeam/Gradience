# theming.py
#
# Change the look of Adwaita, with ease
# Copyright (C) 2023, Gradience Team
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

from gradience.backend.models.preset import Preset


def generate_gtk_css(app_type: str, preset: Preset) -> str:
    variables = preset.variables
    palette = preset.palette
    custom_css = preset.custom_css

    theming_warning = """/*
Generated with Gradience

Issues caused by theming should be reported to Gradience repository, and not to upstream

https://github.com/GradienceTeam/Gradience
*/

"""

    gtk_css = ""

    for key in variables.keys():
        gtk_css += f"@define-color {key} {variables[key]};\n"

    for prefix_key in palette.keys():
        for key in palette[prefix_key].keys():
            gtk_css += f"@define-color {prefix_key + key} {palette[prefix_key][key]};\n"

    gtk_css += custom_css.get(app_type, "")

    gtk_css += "\n.navigation-sidebar {\nbackground-color: "
    gtk_css += variables["window_bg_color"]
    gtk_css += ";\n}"

    final_css = theming_warning + gtk_css

    return final_css
