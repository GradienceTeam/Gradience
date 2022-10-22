import shutil

from gradience.modules.utils import to_slug_case
from .preset import presets_dir, Preset
from .custom_presets import download_preset

import os
from pathlib import Path


class PresetManager:
    def __init__(self):
        self.presets_dir = Path(presets_dir)
        self.presets = {"user": {}, "official": {}, "curated": {}}
        self.populate()

    def populate(self):
        """Populate the presets dictionary with all the presets in the presets directory.
        ```
        .config/presets/
        ├── official
        |   ├── tango.json
        ├── curated
        │   ├── crystal-clear.json
        ├── user
        |   ├── my-preset.json
        ```
        """
        if not os.path.exists(presets_dir):
            os.mkdir(presets_dir)

        for repo in Path(presets_dir).iterdir():
            # .config/presets/official for example
            if repo.is_dir():
                for preset in repo.iterdir():
                    # .config/presets/official/tango.json for example
                    if preset.is_file():
                        self.add_preset(Preset(preset_path=preset), repo.name)
            elif repo.is_file():
                # old presets
                # gradience move them to .config/presets/user
                shutil.move(repo, self.presets_dir / "user" / repo.name)
                self.add_preset(
                    Preset(preset_path=self.presets_dir / "user" / repo.name), "user"
                )

    def add_preset(self, preset, repo_name="user"):
        """Add a preset to the presets dictionary."""
        self.presets[repo_name][preset.name] = preset

    def download(self, preset_name, repo, url):
        """Download a preset from the official repository."""
        download_preset(preset_name, repo, url)
        preset = Preset(
            preset_path=self.presets_dir / repo / to_slug_case(preset_name) + ".json"
        )
        self.add_preset(preset, repo)
