# custom_presets.py
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

import os
import json
import urllib3

from .utils import to_slug_case


# Open an pool manager
poolmgr = urllib3.PoolManager()


def fetch_presets(repo):
    try:
        http = poolmgr.request(
            "GET",
            repo)
        raw = json.loads(http.data)

        preset_dict = {}
        url_list = []

        for data in raw.items():
            data = list(data)
            data.insert(0, to_slug_case(data[0]))

            url = data[2]
            data.pop(2)  # Remove preset URL from list

            to_dict = iter(data)
            # Convert list back to dict
            preset_dict.update(dict(zip(to_dict, to_dict)))

            url_list.append(url)

        return preset_dict, url_list
    except Exception:  # offline
        return False, False


def download_preset(name, url):
    try:
        http = poolmgr.request("GET", url)
        raw = json.loads(http.data)

        data = json.dumps(raw)

        with open(os.path.join(
                os.environ.get("XDG_CONFIG_HOME",
                               os.environ["HOME"] + "/.config"),
                "presets",
                to_slug_case(name) + ".json"),
                "w") as f:
            f.write(data)
            f.close()
    except Exception:
        return False, False
