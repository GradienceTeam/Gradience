# unsupported_shell_version.py
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
from gradience.backend.utils.shell import get_full_shell_version

class GradienceUnsupportedShellVersionDialog(Adw.MessageDialog):
    __gtype_name__ = "GradienceUnsupportedShellVersionDialog"
    
    def __init__(self, parent, **kwargs):
        super().__init__(**kwargs)

        self.parent = parent
        self.app = self.parent.get_application()

        self.set_transient_for(self.app.get_active_window())

        self.set_heading(_(f"Unsupported Shell Version ({get_full_shell_version()})"))
        self.set_body(_("The shell version you are using is not supported. Please upgrade to a newer version of GNOME."))

        self.add_response("ok", _("OK"))
        self.set_default_response("ok")
        self.set_close_response("ok")

   