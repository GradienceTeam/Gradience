from .plugins.gtk4 import AdwcustomizerGtk4Plugin

class AdwcustomizerPluginsList:
    def __init__(self):
        self.plugins = {
            "gtk4": AdwcustomizerGtk4Plugin()
        }

    def load_all_custom_settings(self, settings):
        for plugin_id, plugin in self.plugins.items():
            plugin.load_custom_settings(settings[plugin_id])

    def get_all_custom_settings_for_preset(self):
        custom_settings = {}
        for plugin_id, plugin in self.plugins.items():
            custom_settings[plugin_id] = plugin.get_custom_settings_for_preset()
