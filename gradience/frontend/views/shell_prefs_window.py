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

from gradience.backend.utils.colors import rgb_to_hash
from gradience.backend.constants import rootdir

from gradience.frontend.widgets.option_row import GradienceOptionRow
from gradience.frontend.schemas.shell_schema import shell_schema

from gradience.backend.logger import Logger

logging = Logger()


@Gtk.Template(resource_path=f"{rootdir}/ui/shell_prefs_window.ui")
class GradienceShellPrefsWindow(Adw.PreferencesWindow):
    __gtype_name__ = "GradienceShellPrefsWindow"

    custom_colors_group = Gtk.Template.Child("custom-colors-group")

    def __init__(self, parent, shell_colors: dict, **kwargs):
        super().__init__(**kwargs)

        self.shell_colors = shell_colors

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

            pref_variable.color_value.connect("color-set", self.on_color_value_changed, pref_variable)
            pref_variable.text_value.connect("changed", self.on_text_value_changed, pref_variable)

            self.set_colors(pref_variable, variable)

    def set_colors(self, widget, variable):
        if len(self.shell_colors) != len(shell_schema["variables"]):
            try:
                self.shell_colors[variable["name"]] = variable["default_value"]
            except KeyError:
                try:
                    self.shell_colors[variable["name"]] = self.app.variables[variable["var_name"]]
                except KeyError:
                    raise
            finally:
                widget.update_value(self.shell_colors[variable["name"]])
        else:
            widget.update_value(self.shell_colors[variable["name"]])

    def on_color_value_changed(self, widget, parent, *_args):
        color_name = parent.props.name
        color_value = widget.get_rgba().to_string()

        if color_value.startswith("rgb") or color_value.startswith("rgba"):
            color_hex, alpha = rgb_to_hash(color_value)
            if not alpha:
                color_value = color_hex

        self.shell_colors[color_name] = color_value

    def on_text_value_changed(self, widget, parent, *_args):
        color_name = parent.props.name
        color_value = widget.get_text()

        self.shell_colors[color_name] = color_value
