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

from .utils import to_slug_case, buglog


# Open an pool manager
poolmgr = urllib3.PoolManager()

# TODO: Modify functions to be asynchronous
def fetch_presets(repo) -> [dict, list]:
    try:
        http = poolmgr.request("GET", repo)
    except urllib3.exceptions.NewConnectionError as e: # offline
        buglog(f"Failed to establish a new connection. Exc: {e}")
        return False, False
    except urllib3.exceptions.MaxRetryError as e:
        buglog(f"Maximum number of retries exceeded. Exc: {e}")
        return False, False
    except urllib3.exceptions.HTTPError as e:
        buglog(f"Unhandled urllib3.exceptions.HTTPError error code. Exc: {e}")
        return False, False
    
    try:
        raw = json.loads(http.data)
    except json.JSONDecodeError as e:
        buglog(f"Error with decoding JSON data. Exc: {e}")
        return False, False

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

def download_preset(name, repo_name, url) -> None:
    try:
        http = poolmgr.request("GET", url)
    except urllib3.exceptions.NewConnectionError as e: # offline
        buglog(f"Failed to establish a new connection. Exc: {e}")
        return False, False
    except urllib3.exceptions.MaxRetryError as e:
        buglog(f"Maximum number of retries exceeded. Exc: {e}")
        return False, False
    except urllib3.exceptions.HTTPError as e:
        buglog(f"Unhandled urllib3.exceptions.HTTPError error code. Exc: {e}")
        return False, False

    try:
        raw = json.loads(http.data)
    except json.JSONDecodeError as e:
        buglog(f"Error with decoding JSON data. Exc: {e}")
        return False, False

    data = json.dumps(raw)

    try:
        with open(
            os.path.join(
                os.environ.get("XDG_CONFIG_HOME",
                                os.environ["HOME"] + "/.config"),
                "presets",
                repo_name,
                to_slug_case(name) + ".json",
            ),
            "w",
        ) as f:
            f.write(data)
            f.close()
    except OSError as e:
        buglog(f"Failed to write data to a file. Exc: {e}")
