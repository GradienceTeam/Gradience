# option.py
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

from .constants import rootdir


@Gtk.Template(resource_path=f"{rootdir}/ui/option.ui")
class GradienceOption(Adw.ActionRow):
    __gtype_name__ = "GradienceOption"

    color_value = Gtk.Template.Child("color-value")
    text_value = Gtk.Template.Child("text-value")
    value_stack = Gtk.Template.Child("value-stack")
    text_value_toggle = Gtk.Template.Child("text-value-toggle")
    warning_button = Gtk.Template.Child("warning-button")
    warning_label = Gtk.Template.Child("warning-label")
    explanation_button = Gtk.Template.Child("explanation-button")
    explanation_label = Gtk.Template.Child("explanation-label")

    def __init__(self,
		name,
		title,
		explanation,
		adw_gtk3_support="yes",
		**kwargs
	):
        super().__init__(**kwargs)

        self.set_name(name)
        self.set_title(title)
        self.set_subtitle("@" + name)

        if adw_gtk3_support == "yes":
            self.warning_button.set_visible(False)
        elif adw_gtk3_support == "partial":
            self.warning_button.add_css_class("warning")
            self.warning_label.set_label(
                _("This option is only partially supported by the adw-gtk3 \
					theme.")
            )
        elif adw_gtk3_support == "no":
            self.warning_button.add_css_class("error")
            self.warning_label.set_label(
                _("This option is not supported by the adw-gtk3 theme.")
            )

        self.explanation_label.set_label(explanation or "")
        if explanation is None:
            self.explanation_button.set_visible(False)

    @Gtk.Template.Callback()
    def on_color_value_changed(self, *_args):
        self.update_value(
            self.color_value.get_rgba().to_string(), update_from="color_value"
        )

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
                self.color_value.set_tooltip_text(
                    _("Not a color, see text value"))

        if (
            Gtk.Application.get_default().is_ready
            and kwargs.get("update_from") == "text_value"
            and new_value != ""
        ):
            Gtk.Application.get_default(
            ).variables[self.get_name()] = new_value
            Gtk.Application.get_default().mark_as_dirty()
            Gtk.Application.get_default().reload_variables()
