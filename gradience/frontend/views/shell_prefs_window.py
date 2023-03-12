# shell_prefs_window.py
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

from gi.repository import Gtk, Adw

from gradience.backend.constants import rootdir

from gradience.frontend.widgets.option_row import GradienceOptionRow
from gradience.frontend.schemas.shell_schema import shell_schema

from gradience.backend.logger import Logger

logging = Logger()


@Gtk.Template(resource_path=f"{rootdir}/ui/shell_prefs_window.ui")
class GradienceShellPrefsWindow(Adw.PreferencesWindow):
    __gtype_name__ = "GradienceShellPrefsWindow"

    custom_colors_group = Gtk.Template.Child("custom-colors-group")

    def __init__(self, parent, **kwargs):
        super().__init__(**kwargs)

        self.parent = parent
        self.settings = parent.settings
        self.app = self.parent.get_application()

        self.set_transient_for(self.app.get_active_window())

        self.setup()

    def setup(self):
        for variable in shell_schema["variables"]:
            pref_variable = GradienceOptionRow(
                variable["name"],
                variable["title"]
                #variable.get("explanation")
            )
            self.custom_colors_group.add(pref_variable)

            #pref_variable.connect_signals(update_vars=False)

            try:
                self.app.custom_colors[variable["name"]] = variable["default_value"]
            except KeyError:
                try:
                    self.app.custom_colors[variable["name"]] = self.app.variables[variable["var_name"]]
                except KeyError:
                    raise
            finally:
                pref_variable.update_value(self.app.custom_colors[variable["name"]], update_var=self.app.custom_colors)

