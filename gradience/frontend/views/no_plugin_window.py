# no_plugin_window.py
#
# Change the look of Adwaita, with ease
# Copyright (C) 2022-2023, Gradience Team
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

from gi.repository import Gtk, Adw

from gradience.backend.constants import rootdir


@Gtk.Template(resource_path=f"{rootdir}/ui/no_plugin_window.ui")
class GradienceNoPluginPrefWindow(Adw.PreferencesWindow):
    __gtype_name__ = "GradienceNoPluginPrefWindow"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
