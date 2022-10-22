from pickletools import string1
import shutil

from gradience.modules.utils import to_slug_case
from .preset import presets_dir, Preset
from .custom_presets import download_preset, fetch_presets, get_as_json
from .exceptions import GradienceError

import os
from pathlib import Path
import semver

BASE_COMMUNITY_URL = "https://raw.githubusercontent.com/GradienceTeam/Community-experiment/next/"
CURATED_PRESETS_URL = BASE_COMMUNITY_URL + "curated/{}.json"
OFFICIAL_PRESETS_URL = BASE_COMMUNITY_URL + "official/{}.json"

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
                        self.add_preset(Preset(preset_path=preset, repo=repo.name), repo.name)
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

    def download(self, preset_name, repo, url=None):
        """Download a preset from the official repository."""
        preset_name = to_slug_case(preset_name)
        if url is None:
            if repo == "official":
                url = OFFICIAL_PRESETS_URL.format(preset_name)
            elif repo == "curated":
                url = CURATED_PRESETS_URL.format(preset_name)
        download_preset(preset_name, repo, url)
        preset = Preset(
            preset_path=self.presets_dir / repo / f"{to_slug_case(preset_name)}.json", repo=repo
        )
        self.add_preset(preset, repo)

    def update_all(self):
        for repo in self.presets:
            self.update_repo(repo)

    def update(self, preset: Preset):
        print(print(f"Updating {preset.name}..."))
        url = preset.url
        status, data_online = get_as_json(url)
        if status:
            try:
                version = semver.parse_version_info(data_online["version"])
                if version != preset.version:
                    preset.update_from_json(data_online)
            except TypeError:
                raise GradienceError("Presets must have a version attribute.")
        else:
            raise GradienceError(f"Could not update {preset.name}.")


    def update_repo(self, repo: str):
        if repo == "user": # user repo is not updated
            return
        for preset in self.presets[repo].values():
            self.update(preset)
