# repo.py
#
# Change the look of Adwaita, with ease
# Copyright (C) 2022 Gradience Team
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
        print("get presets in Repo")
        presets = {}
        for preset in os.listdir(self.path):
            print(preset)
            if preset.endswith(".json"):
                presets[preset[:-5]] = Preset(os.path.join(self.path, preset))
        return presets
