# option_row.py
#
# Change the look of Adwaita, with ease
# Copyright (C) 2022-2023, Gradience Team
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

from gradience.backend.utils.colors import rgb_to_hash
from gradience.backend.constants import rootdir


@Gtk.Template(resource_path=f"{rootdir}/ui/option_row.ui")
class GradienceOptionRow(Adw.ActionRow):
    __gtype_name__ = "GradienceOptionRow"

    color_value = Gtk.Template.Child("color-value")
    text_value = Gtk.Template.Child("text-value")
    value_stack = Gtk.Template.Child("value-stack")
    text_value_toggle = Gtk.Template.Child("text-value-toggle")
    warning_button = Gtk.Template.Child("warning-button")
    warning_label = Gtk.Template.Child("warning-label")
    explanation_button = Gtk.Template.Child("explanation-button")
    explanation_label = Gtk.Template.Child("explanation-label")

    def __init__(self, name, title, explanation=None, adw_gtk3_support=None, update_var=None, **kwargs):
        super().__init__(**kwargs)

        self.app = Gtk.Application.get_default()

        self.set_name(name)
        self.set_title(title)
        self.set_subtitle("@" + name)

        if adw_gtk3_support == "yes" or not adw_gtk3_support:
            self.warning_button.set_visible(False)
        elif adw_gtk3_support == "partial":
            self.warning_button.add_css_class("warning")
            self.warning_label.set_label(
                _("This option is only partially supported by adw-gtk3.")
            )
        elif adw_gtk3_support == "no":
            self.warning_button.add_css_class("error")
            self.warning_label.set_label(
                _("This option is not supported by adw-gtk3.")
            )

        self.explanation_label.set_label(explanation or "")

        if not explanation:
            self.explanation_button.set_visible(False)

        self.update_var = update_var

    def connect_signals(self, update_vars):
        self.color_value.connect("color-set", self.on_color_value_changed, update_vars)
        self.text_value.connect("changed", self.on_text_value_changed, update_vars)

    def on_color_value_changed(self, _unused, update_vars, *_args):
        color_value = self.color_value.get_rgba().to_string()

        if color_value.startswith("rgb") or color_value.startswith("rgba"):
            color_hex, alpha = rgb_to_hash(color_value)
            if not alpha:
                color_value = color_hex

        self.update_value(
            color_value, update_from="color_value", update_vars=update_vars
        )

    def on_text_value_changed(self, _unused, update_vars, *_args):
        color_value = self.text_value.get_text()

        self.update_value(
            color_value, update_from="text_value", update_vars=update_vars
        )

    @Gtk.Template.Callback()
    def on_text_value_toggled(self, *_args):
        widget = self.text_value if self.text_value_toggle.get_active() else self.color_value
        self.value_stack.set_visible_child(widget)
        self.set_activatable_widget(widget)
        
        tooltip = _("Show Color") if self.text_value_toggle.get_active() else _("Show Hex")
        self.text_value_toggle.set_tooltip_text(tooltip);

    def update_value(self, new_value, update_vars=False, **kwargs):
        rgba = Gdk.RGBA()
        is_app_ready = self.app.is_ready

        if kwargs.get("update_from") != "text_value":
            if rgba.parse(new_value):
                self.text_value.set_text(new_value)
                self.text_value_toggle.set_active(False)
            else:
                self.text_value.set_text(new_value)
                self.text_value_toggle.set_active(True)

        if kwargs.get("update_from") != "color_value":
            if rgba.parse(new_value):
                self.color_value.set_rgba(rgba)
                self.color_value.set_tooltip_text(new_value)
            else:
                rgba.parse("rgba(0,0,0,0)")
                self.color_value.set_rgba(rgba)
                self.color_value.set_tooltip_text(_("Not a color, see text value"))

        if update_vars == True:
            if is_app_ready and kwargs.get("update_from") == "text_value" and new_value != "":
                if self.update_var:
                    self.update_var[self.get_name()] = new_value
                else:
                    self.app.variables[self.get_name()] = new_value
                self.app.mark_as_dirty()
                self.app.reload_variables()
