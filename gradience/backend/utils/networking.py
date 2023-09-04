# networking.py
#
# Change the look of Adwaita, with ease
# Copyright (C) 2023, Gradience Team
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

from urllib.parse import urlparse


def get_preset_repos(use_jsdelivr: bool) -> dict:
    if use_jsdelivr:
        from gradience.backend.globals import preset_repos_jsdelivr
        preset_repos = preset_repos_jsdelivr
    else:
        from gradience.backend.globals import preset_repos_github
        preset_repos = preset_repos_github

    return preset_repos

def github_to_jsdelivr_url(github_url: str) -> str:
    """
    Converts Github raw data URL link to JSDelivr CDN link.
    """

    jsdelivr_url = None

    # https://github.com/GradienceTeam/Community/raw/next/official/builder.json =>
    # https://cdn.jsdelivr.net/gh/GradienceTeam/Community@next/official/builder.json
    if "https://github.com" in github_url:
        JSDELIVER_FORMAT = "https://cdn.jsdelivr.net/gh/{user}/{repo}@{branch}/{path}"
        path = urlparse(github_url).path
        user, repo, _, branch, *path = path.strip('/').split('/')
        path = "/".join(path)
        jsdelivr_url = JSDELIVER_FORMAT.format(user=user, repo=repo, branch=branch, path=path)

    return jsdelivr_url
