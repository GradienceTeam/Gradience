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

from dataclasses import dataclass
from importlib import import_module
import os
import sys
import importlib.util


@dataclass
class Meta:
    name: str
    description: str
    version: str

    def __str__(self) -> str:
        return f'{self.name}: {self.version}'


class IPluginRegistry(type):
    plugin_registries = list()

    def __init__(cls, name, bases, attrs):
        super().__init__(cls)
        if name != 'AdwcustomizerPluginCore':
            IPluginRegistry.plugin_registries.append(cls)


class AdwcustomizerPluginCore(metaclass=IPluginRegistry):
    meta: Meta

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


class PluginUseCase:
    def __init__(self, directory) -> None:
        self.plugins_package = directory
        self.modules = []

    def __check_loaded_plugin_state(self, plugin_module):
        if len(IPluginRegistry.plugin_registries) > 0:
            latest_module = IPluginRegistry.plugin_registries[-1]
            latest_module_name = latest_module.__module__
            current_module_name = plugin_module.__name__
            if current_module_name == latest_module_name:
                print(f'Successfully imported module `{current_module_name}`')
                self.modules.append(latest_module)
            else:
                print(
                    f'Expected to import -> `{current_module_name}` but got -> `{latest_module_name}`'
                )
            # clear plugins from the registry when we're done with them
            IPluginRegistry.plugin_registries.clear()
        else:
            print(f'No plugin found in registry for module: {plugin_module}')

    def __search_for_plugins_in(self, plugins_path, package_name):
        print(f"plugins path: {plugins_path}")
        sys.path.append(plugins_path)

        for m in os.listdir(plugins_path):
            module = import_module(m)
            self.__check_loaded_plugin_state(module)
            print(dir(module))

    def discover_plugins(self, reload: bool):
        """
        Discover the plugin classes contained in Python files, given a
        list of directory names to scan.
        """
        if reload:
            print("Reload")
            self.modules.clear()
            IPluginRegistry.plugin_registries.clear()
            print(
                f'Searching for plugins under package {self.plugins_package}')
            package_name = os.path.basename(
                os.path.normpath(self.plugins_package))
            self.__search_for_plugins_in(self.plugins_package, package_name)

    @staticmethod
    def register_plugin(module: type, logger) -> AdwcustomizerPluginCore:
        """
        Create a plugin instance from the given module
        :param module: module to initialize
        :param logger: logger for the module to use
        :return: a high level plugin
        """
        return module(logger)

    @staticmethod
    def hook_plugin(plugin: AdwcustomizerPluginCore):
        """
        Return a function accepting commands.
        """
        return plugin.invoke


class PluginEngine:
    def __init__(self, **args) -> None:
        self.use_case = PluginUseCase(os.path.join(
            os.environ["HOME"],
            ".gradience_plugins"))

    def start(self) -> None:
        self.__reload_plugins()
        self.__invoke_on_plugins('Q')

    def __reload_plugins(self) -> None:
        """Reset the list of all plugins and initiate the walk over the main
        provided plugin package to load all available plugins
        """
        self.use_case.discover_plugins(True)

    def __invoke_on_plugins(self, command: chr):
        """Apply all of the plugins on the argument supplied to this function
        """
        for module in self.use_case.modules:
            plugin = self.use_case.register_plugin(module)
            delegate = self.use_case.hook_plugin(plugin)
            plugin = delegate(command=command)
            print(f'Loaded plugin: {plugin}')


if __name__ == "__main__":
    import sys
    sys.path.append("/usr/local/lib/python3.10/site-packages/")
    engine = PluginEngine()
    engine.start()
