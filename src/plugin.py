from .setting import AdwcustomizerSetting

class AdwcustomizerPlugin:
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
            setting_dict[setting_key] = setting.value
        return setting_list

    def get_alias_values(self):
        alias_values = {}
        for key, value in self.alias_dict.items():
            alias_values[key] = self.colors.get(value, self.palette.get(value, self.custom_settings.get(value)))
        return alias_values

    def validate(self):
        pass

    def apply(self):
        pass