# window.py
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

from gi.repository import Gtk
from .error import AdwcustomizerError

@Gtk.Template(resource_path='/com/github/ArtyIF/AdwCustomizer/ui/window.ui')
class AdwcustomizerMainWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'AdwcustomizerMainWindow'

    content = Gtk.Template.Child()
    save_preset_button = Gtk.Template.Child("save-preset-button")
    presets_dropdown = Gtk.Template.Child("presets-dropdown")
    presets_menu = Gtk.Template.Child("presets-menu")
    errors_button = Gtk.Template.Child("errors-button")
    errors_list = Gtk.Template.Child("errors-list")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.presets_dropdown.get_popover().connect("show", self.on_presets_dropdown_activate)

    def update_errors(self, errors):
        child = self.errors_list.get_row_at_index(0)
        while child is not None:
            self.errors_list.remove(child)
            child = self.errors_list.get_row_at_index(0)
        self.errors_button.set_visible(len(errors) > 0)
        for error in errors:
            self.errors_list.append(AdwcustomizerError(error["error"], error["element"], error["line"]))

    def on_presets_dropdown_activate(self, *args):
        self.get_application().reload_user_defined_presets()
