# palette_shades.py
#
# Change the look of Adwaita, with ease
# Copyright (C) 2022  Gradience Team
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

from gi.repository import Gtk, Gdk, Adw

from gradience.backend.constants import rootdir


@Gtk.Template(resource_path=f"{rootdir}/ui/palette_shades.ui")
class GradiencePaletteShades(Adw.ActionRow):
    __gtype_name__ = "GradiencePaletteShades"

    def __init__(self, prefix, color_title, n_shades, **kwargs):
        super().__init__(**kwargs)

        self.prefix = prefix
        self.set_name(prefix + "shades")
        self.set_title(color_title)
        self.set_subtitle("@" + prefix + "[1, " + str(n_shades) + "]")

        self.color_pickers = {}
        for i in range(1, n_shades + 1):
            picker = Gtk.ColorButton()
            picker.set_name(prefix + str(i))
            picker.set_rgba(Gdk.RGBA(red=0, green=0, blue=0, alpha=0))
            picker.set_valign(Gtk.Align.CENTER)
            picker.connect("color-set", self.on_color_changed)
            self.color_pickers[str(i)] = picker
            self.add_suffix(picker)

    def on_color_changed(self, *_args):
        shades = {}
        for picker_key, picker in self.color_pickers.items():
            shades[picker_key] = picker.get_rgba().to_string()
        self.update_shades(shades, update_from="color_value")

    def update_shades(self, shades, **kwargs):
        for i in range(1, len(shades) + 1):
            new_rgba = Gdk.RGBA()
            if new_rgba.parse(shades[str(i)]):
                self.color_pickers[str(i)].set_rgba(new_rgba)
                self.color_pickers[str(i)].set_tooltip_text(shades[str(i)])
            if (
                Gtk.Application.get_default().is_ready
                and kwargs.get("update_from") == "color_value"
            ):
                Gtk.Application.get_default().palette[self.prefix][str(i)] = shades[
                    str(i)
                ]

        if (
            Gtk.Application.get_default().is_ready
            and kwargs.get("update_from") == "color_value"
        ):
            Gtk.Application.get_default().mark_as_dirty()
            Gtk.Application.get_default().reload_variables()
