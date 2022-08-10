from .plugins.gtk4 import AdwcustomizerGtk4Plugin
import os
from pathlib import Path
import importlib
class AdwcustomizerPluginsList:
    def __init__(self):
        self.plugins = { # AdwCustomizerTeam plugins
            "gtk4": AdwcustomizerGtk4Plugin()
        }
        self.add_user_plugins()

    def add_user_plugins(self):
        self.user_plugin_dir = Path(os.environ.get("XDG_DATA_HOME", os.environ["HOME"])) / ".local" / "share" / "AdwCustomizer" / "plugins"
        if self.user_plugin_dir.exists():
            for path, _, name in os.walk(self.user_plugin_dir):
                print(name[0])
        else:
            print("No plugins dir found")


    def load_all_custom_settings(self, settings):
        for plugin_id, plugin in self.plugins.items():
            plugin.load_custom_settings(settings[plugin_id])

    def get_all_custom_settings_for_preset(self):
        custom_settings = {}
        for plugin_id, plugin in self.plugins.items():
            custom_settings[plugin_id] = plugin.get_custom_settings_for_preset()