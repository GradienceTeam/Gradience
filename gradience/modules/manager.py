from pickletools import string1
import shutil

from gradience.modules.utils import to_slug_case
from .preset import presets_dir, Preset
from .custom_presets import download_preset, fetch_presets, get_as_json

import os
from pathlib import Path
import semver

class PresetManager:
    def __init__(self, user_repo={}):
        self.presets_dir = Path(presets_dir)
        self.presets = {"user": {}, "official": {}, "curated": {}, **user_repo}
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

    def update_all(self):
        for repo in self.presets:
            self.update_repo(repo)

    def update(self, preset: Preset):
        url = preset.url
        data_online = get_as_json(url)
        version = semver.Version.parse(data_online["version"])
        if version != preset.version:
            preset.update_from_json(data_online)


    def update_repo(self, repo: str):
        if repo == "user": # user repo is not updated
            return
        for preset in self.presets[repo]:
            self.update(preset)
