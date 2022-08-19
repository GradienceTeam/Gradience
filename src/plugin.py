# plugin.py
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

#from .setting import AdwcustomizerSetting

class GradiencePluginCore():
    def __init__(self):
        self.title = None

        self.colors = None
        self.palette = None

        # Custom settings shown on a separate view
        self.custom_settings = {}
        # A dict to alias parameters to different names
        # Key is the alias name, value is the parameter name
        # Parameter can be any key in colors, palette or custom settings
        self.alias_dict = {}

    def update_builtin_parameters(self, colors, palette):
        self.colors = colors
        self.palette = palette

    def load_custom_settings(self, settings):
        for setting_key, setting in self.custom_settings:
            self.custom_settings[setting_key].set_value(settings[setting_key])

    def get_custom_settings_for_preset(self):
        setting_dict = {}
        for setting_key, setting in self.custom_settings:
            return setting_dict[setting_key]

    def get_alias_values(self):
        alias_values = {}
        for key, value in self.alias_dict.items():
            alias_values[key] = self.colors.get(
                value, self.palette.get(value, self.custom_settings.get(value))
            )
        return alias_values

    def validate(self):
        raise NotImplementedError()

    def apply(self, dark_theme=False):
        raise NotImplementedError()

    def save(self):
        raise NotImplementedError()

