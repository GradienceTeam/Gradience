# palette_shades.py
#
# Copyright 2022 Adwaita Manager Team
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE X CONSORTIUM BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# Except as contained in this notice, the name(s) of the above copyright
# holders shall not be used in advertising or otherwise to promote the sale,
# use or other dealings in this Software without prior written
# authorization.

from gi.repository import Gtk, Gdk, Adw

@Gtk.Template(resource_path='/com/github/AdwCustomizerTeam/AdwCustomizer/ui/palette_shades.ui')
class AdwcustomizerPaletteShades(Adw.ActionRow):
    __gtype_name__ = 'AdwcustomizerPaletteShades'

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
            if Gtk.Application.get_default().is_ready and kwargs.get("update_from") == "color_value":
                Gtk.Application.get_default().palette[self.prefix][str(i)] = shades[str(i)]

        if Gtk.Application.get_default().is_ready and kwargs.get("update_from") == "color_value":
            Gtk.Application.get_default().mark_as_dirty()
            Gtk.Application.get_default().reload_variables()
