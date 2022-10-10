from gradience.utils.utils import to_slug_case
from gradience.utils.preset import Preset, presets_dir
import os


class Repo:
    presets = {}

    def __init__(self, name):
        self.name = to_slug_case(name)
        self.path = os.path.join(presets_dir, name)
        self.presets = self.get_presets()

    def get_presets(self):
        presets = {}
        for preset in os.listdir(self.path):
            if preset.endswith(".json"):
                presets[preset[:-5]] = Preset(preset[:-5], self.name)
        return presets
