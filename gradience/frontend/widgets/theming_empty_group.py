# theming_empty_group.py
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

from enum import Enum

from gi.repository import Adw, Gio, GLib, Gtk

from gradience.backend.constants import rootdir
from gradience.backend.exceptions import UnsupportedShellVersion
from gradience.backend.logger import Logger
from gradience.backend.theming.shell import ShellTheme

from gradience.frontend.views.shell_prefs_window import GradienceShellPrefsWindow

logging = Logger()


@Gtk.Template(resource_path=f"{rootdir}/ui/theming_empty_group.ui")
class GradienceEmptyThemingGroup(Adw.PreferencesGroup):
    __gtype_name__ = "GradienceEmptyThemingGroup"

    def __init__(self, parent, **kwargs):
        super().__init__(**kwargs)

        self.parent = parent
        self.settings = parent.settings
        self.app = self.parent.get_application()

        self.setup_signals()
        self.setup()

    def setup_signals(self):
        pass

    def setup(self):
        pass
