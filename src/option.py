# option.py
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

@Gtk.Template(resource_path='/com/github/ArtyIF/AdwCustomizer/ui/option.ui')
class AdwcustomizerOption(Adw.ActionRow):
    __gtype_name__ = 'AdwcustomizerOption'

    color_value = Gtk.Template.Child("color-value")
    text_value = Gtk.Template.Child("text-value")
    value_stack = Gtk.Template.Child("value-stack")
    text_value_toggle = Gtk.Template.Child("text-value-toggle")
    warning_button = Gtk.Template.Child("warning-button")
    warning_label = Gtk.Template.Child("warning-label")
    explanation_button = Gtk.Template.Child("explanation-button")
    explanation_label = Gtk.Template.Child("explanation-label")

    def __init__(self, name, title, adw_gtk3_support, explanation, **kwargs):
        super().__init__(**kwargs)

        self.set_name(name)
        self.set_title(title)
        self.set_subtitle("@" + name)

        if adw_gtk3_support == "yes":
            self.warning_button.set_visible(False)
        elif adw_gtk3_support == "partial":
            self.warning_button.add_css_class("warning")
            self.warning_label.set_label(_("This option is only partially supported by the adw-gtk3 theme."))
        elif adw_gtk3_support == "no":
            self.warning_button.add_css_class("error")
            self.warning_label.set_label(_("This option is not supported by the adw-gtk3 theme."))

        self.explanation_label.set_label(explanation or "")
        if explanation is None:
            self.explanation_button.set_visible(False)

    @Gtk.Template.Callback()
    def on_color_value_changed(self, *_args):
        self.update_value(self.color_value.get_rgba().to_string(), update_from="color_value")

    @Gtk.Template.Callback()
    def on_text_value_changed(self, *_args):
        self.update_value(self.text_value.get_text(), update_from="text_value")

    @Gtk.Template.Callback()
    def on_text_value_toggled(self, *_args):
        if self.text_value_toggle.get_active():
            self.value_stack.set_visible_child(self.text_value)
        else:
            self.value_stack.set_visible_child(self.color_value)

    def update_value(self, new_value, **kwargs):
        rgba = Gdk.RGBA()
        if kwargs.get("update_from") != "text_value":
            if rgba.parse(new_value):
                self.text_value.set_text(rgba.to_string())
            else:
                self.text_value.set_text(new_value)
        if kwargs.get("update_from") != "color_value":
            if rgba.parse(new_value):
                self.color_value.set_rgba(rgba)
                self.color_value.set_tooltip_text(new_value)
                if kwargs.get("update_from") != "text_value":
                    self.text_value_toggle.set_active(False)
            elif kwargs.get("update_from") != "text_value":
                self.text_value_toggle.set_active(True)
            else:
                rgba.parse("rgba(0,0,0,0)")
                self.color_value.set_rgba(rgba)
                self.color_value.set_tooltip_text(_("Not a color, see text value"))

        if Gtk.Application.get_default().is_ready and kwargs.get("update_from") == "text_value" and new_value != "":
            Gtk.Application.get_default().variables[self.get_name()] = new_value
            Gtk.Application.get_default().mark_as_dirty()
            Gtk.Application.get_default().reload_variables()
