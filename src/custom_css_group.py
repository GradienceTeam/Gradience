# custom_css_group.py
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

from gi.repository import Gtk, Adw

@Gtk.Template(resource_path='/com/github/ArtyIF/AdwCustomizer/ui/custom_css_group.ui')
class AdwcustomizerCustomCSSGroup(Adw.PreferencesGroup):
    __gtype_name__ = 'AdwcustomizerCustomCSSGroup'

    app_type_dropdown = Gtk.Template.Child("app-type-dropdown")
    custom_css_text_view = Gtk.Template.Child("custom-css-text-view")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.custom_css = {}

    def load_custom_css(self, custom_css):
        self.custom_css = custom_css
        self.custom_css_text_view.get_buffer().set_text(list(self.custom_css.values())[self.app_type_dropdown.get_selected()])

    @Gtk.Template.Callback()
    def on_custom_css_changed(self, buffer):
        Gtk.Application.get_default().update_custom_css_text(list(self.custom_css.keys())[self.app_type_dropdown.get_selected()], buffer.props.text)

    @Gtk.Template.Callback()
    def on_dropdown_notify(self, _, pspec):
        if pspec.name == "selected":
            self.custom_css_text_view.get_buffer().set_text(list(self.custom_css.values())[self.app_type_dropdown.get_selected()])
