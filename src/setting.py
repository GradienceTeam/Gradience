# setting.py
#
# Change the look of Adwaita, with ease
# Copyright (C) 2022  Gradience Team
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


class AdwcustomizerSetting:
    def __init__(self, name, title, value_type, explanation=None, default_value=None):
        # TODO supported types:
        #  text
        #  integer
        #  float
        #  color only
        #  color shades
        #  color and text
        #  code field
        self.name = name
        self.title = title
        self.value_type = value_type
        self.explanation = explanation
        self.value = default_value

    def set_value(self, new_value):
        # TODO checks
        self.value = new_value
