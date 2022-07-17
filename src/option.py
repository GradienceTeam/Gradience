# window.py
#
# Copyright 2022 ArtyIF
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

from gi.repository import Gtk, Gdk, Gio, Adw
import json

@Gtk.Template(resource_path='/com/github/ArtyIF/AdwCustomizer/ui/option.ui')
class AdwcustomizerOption(Adw.ActionRow):
    __gtype_name__ = 'AdwcustomizerOption'

    color_value = Gtk.Template.Child("color-value")
    text_value = Gtk.Template.Child("text-value")
    value_stack = Gtk.Template.Child("value-stack")
    text_value_toggle = Gtk.Template.Child("text-value-toggle")
    explanation_button = Gtk.Template.Child("explanation-button")
    explanation_label = Gtk.Template.Child("explanation-label")

    def __init__(self, title, explanation, value, **kwargs):
        super().__init__(**kwargs)

        self.set_title(title)
        self.explanation_label.set_label(explanation or "")
        if (explanation is None):
            self.explanation_button.set_visible(False)

        self.update_value(value)

    @Gtk.Template.Callback()
    def on_text_value_toggled(self, *args):
        if (self.text_value_toggle.get_active()):
            self.value_stack.set_visible_child(self.text_value)
        else:
            self.value_stack.set_visible_child(self.color_value)

    def update_value(self, new_value):
        self.text_value.set_text(new_value)
        rgba = Gdk.RGBA()
        if rgba.parse(new_value):
            self.color_value.set_rgba(rgba)
            self.text_value_toggle.set_active(False)
        else:
            self.text_value_toggle.set_active(True)


