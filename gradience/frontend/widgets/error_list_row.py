# error_list_row.py
#
# Change the look of Adwaita, with ease
# Copyright (C) 2022  Adwaita Manager Team
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

from gi.repository import Gtk

from gradience.backend.constants import rootdir


@Gtk.Template(resource_path=f"{rootdir}/ui/error_list_row.ui")
class GradienceErrorListRow(Gtk.ListBoxRow):
    __gtype_name__ = "GradienceErrorListRow"

    error_label = Gtk.Template.Child("error-label")
    element_label = Gtk.Template.Child("element-label")
    line_label = Gtk.Template.Child("line-label")

    def __init__(self, error, element, line, **kwargs):
        super().__init__(**kwargs)

        self.error_label.set_label(error)
        self.element_label.set_label(element)
        self.line_label.set_label(line)
