from .utils import buglog, to_slug_case
from .preset import Preset
import os

PRESET_DIR = os.path.join(
    os.environ.get("XDG_CONFIG_HOME", os.environ["HOME"] + "/.config"),
    "presets",
)


class Repo:
    presets = {}

    def __init__(self, name):
        self.name = to_slug_case(name)
        self.path = os.path.join(PRESET_DIR, name)
        self.presets = self.get_presets()

    def get_presets(self):
        presets = {}
        for preset in os.listdir(self.path):
            if preset.endswith(".json"):
                presets[preset[:-5]] = Preset(preset[:-5], self.name)
        return presets
