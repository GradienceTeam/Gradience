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

from .utils import to_slug_case, buglog


import aiohttp
import asyncio


async def main(repo):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(repo) as http:
                try:
                    raw = json.loads(await http.text())
                except json.JSONDecodeError as error:
                    buglog(f"Error with decoding JSON data. Exc: {error}")
                    return False, False
        except aiohttp.ClientError as error:
            buglog(f"Failed to establish a new connection. Exc: {error}")
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


# TODO: Modify functions to be asynchronous


def fetch_presets(repo) -> [dict, list]:
    return asyncio.run(main(repo))


async def _download_preset(name, repo_name, url) -> None:
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as http:
                try:
                    raw = json.loads(await http.text())
                except json.JSONDecodeError as error:
                    buglog(f"Error with decoding JSON data. Exc: {error}")
                    return False, False
        except aiohttp.ClientError as error:
            buglog(f"Failed to establish a new connection. Exc: {error}")
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
                encoding="utf-8",
            ) as f:
                f.write(data)
                f.close()
        except OSError as error:
            buglog(f"Failed to write data to a file. Exc: {error}")


def download_preset(name, repo_name, url) -> None:
    asyncio.run(_download_preset(name, repo_name, url))
