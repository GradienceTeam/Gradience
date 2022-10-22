import itertools
import random

import pluggy

from ..preset import Preset
from . import hookspecs

from gradience.constants import pkgdatadir
import os

USER_PLUGIN_DIR = os.path.join(
    os.environ.get("XDG_DATA_HOME", os.environ["HOME"] + "/.local/share"),
    "gradience",
    "plugins",
)

SYSTEM_PLUGIN_DIR = os.path.join(
    pkgdatadir,
    "plugins",
)


def setup_pm():
    plugin_manager = get_plugin_manager()
    plugin_manager = PluginManager(plugin_manager.hook)
    plugin_manager.check()
    return plugin_manager


def get_plugin_manager():
    plugin_manager = pluggy.PluginManager("gradience")
    plugin_manager.add_hookspecs(hookspecs)
    plugin_manager.load_setuptools_entrypoints("gradience")
    plugin_manager.register(SYSTEM_PLUGIN_DIR)
    plugin_manager.register(USER_PLUGIN_DIR)
    return plugin_manager


class PluginManager:
    def __init__(self, hook):
        self.hook = hook

    def apply(self, preset: Preset):
        results = self.hook.apply(preset)

    def validate(self, preset: Preset):
        results = self.hook.validate(preset)

    def enable_all(self):
        return self.hook.enable()

    def disable_all(self):
        return self.hook.disable()

    def check(self):
        return self.hook.check()

    def save(self, preset: Preset):
        results = self.hook.save(preset)
