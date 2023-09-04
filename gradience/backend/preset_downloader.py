# preset_downloader.py
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

from gi.repository import GLib, Soup

from gradience.backend.globals import presets_dir
from gradience.backend.utils.networking import github_to_jsdelivr_url
from gradience.backend.utils.common import to_slug_case

from gradience.backend.logger import Logger

logging = Logger()


class PresetDownloader:
    def __init__(self, use_jsdelivr=False):
        self.use_jsdelivr = use_jsdelivr
        # Open Soup3 session
        self.session = Soup.Session()

    def fetch_presets(self, repo) -> [dict, list]:
        logging.debug(f"Accessing URL address: {repo}")

        try:
            request = Soup.Message.new("GET", repo)
            body = self.session.send_and_read(request, None)
        except GLib.GError as e:
            if e.code == 1: # offline
                logging.error("Failed to establish a new connection.", exc=e)
                raise
            else:
                logging.error(f"Unhandled Libsoup3 GLib.GError error code {e.code}.", exc=e)
                raise
        try:
            raw = json.loads(body.get_data())
        except json.JSONDecodeError as e:
            logging.error("Error while decoding JSON data.", exc=e)
            raise

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

            if self.use_jsdelivr:
                url = github_to_jsdelivr_url(url)

            url_list.append(url)

        return preset_dict, url_list

    def download_preset(self, name, repo_name, repo) -> None:
        logging.debug(f"Accessing URL address: {repo}")

        try:
            request = Soup.Message.new("GET", repo)
            body = self.session.send_and_read(request, None)
        except GLib.GError as e:
            if e.code == 1: # offline
                logging.error("Failed to establish a new connection.", exc=e)
                raise
            else:
                logging.error(f"Unhandled Libsoup3 GLib.GError error code {e.code}.", exc=e)
                raise
        try:
            raw = json.loads(body.get_data())
        except json.JSONDecodeError as e:
            logging.error("Error while decoding JSON data.", exc=e)
            raise

        data = json.dumps(raw, indent=4)

        try:
            with open(
                os.path.join(
                    presets_dir,
                    repo_name,
                    to_slug_case(name) + ".json",
                ),
                "w",
                encoding="utf-8",
            ) as f:
                f.write(data)
                f.close()
        except OSError as e:
            logging.error("Failed to write data to a file.", exc=e)
            raise
