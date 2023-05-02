# shell_schema.py
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

shell_schema = {
    "variables": [
        {
            "name": "bg_color",
            "var_name": "window_bg_color",
            "title": _("Base Background Color")
        },
        {
            "name": "fg_color",
            "var_name": "window_fg_color",
            "title": _("Base Foreground Color")
        },
        {
            "name": "system_bg_color",
            "var_name": "window_bg_color",
            "title": _("Overview Background Color")
        },
        {
            "name": "selected_bg_color",
            "var_name": "accent_bg_color",
            "title": _("Accent Background Color")
        },
        {
            "name": "selected_fg_color",
            "var_name": "window_fg_color",
            "title": _("Accent Foreground Color")
        },
        # TODO: Fix panel background color injection code
        #{
        #    "name": "panel_bg_color",
        #    "var_name": "panel_bg_color",
        #    "title": _("Panel Background Color"),
        #    "default_value": "#000"
        #},
        #{
        #    "name": "osd_bg_color",
        #    "var_name": "window_bg_color",
        #    "title": _("OSD Background Color")
        #},
        {
            "name": "osd_fg_color",
            "var_name": "window_fg_color",
            "title": _("OSD Foreground Color")
        }
    ]
}
