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

from gi.repository import Gtk, Adw

@Gtk.Template(resource_path='/com/github/AdwCustomizerTeam/AdwCustomizer/ui/app_type_dialog.ui')
class AdwcustomizerAppTypeDialog(Adw.MessageDialog):
    __gtype_name__ = 'AdwcustomizerAppTypeDialog'

    gtk4_app_type = Gtk.Template.Child("gtk4-app-type")
    gtk3_app_type = Gtk.Template.Child("gtk3-app-type")

    def __init__(self, heading, body, ok_response_name, ok_response_label, ok_response_appearance, **kwargs):
        super().__init__(**kwargs)
        self.set_heading(heading)
        self.set_body(body)

        self.add_response("cancel", _("Cancel"))
        self.add_response(ok_response_name, ok_response_label)
        self.set_response_appearance(ok_response_name, ok_response_appearance)
        self.set_default_response("cancel")
        self.set_close_response("cancel")

    def get_app_types(self):
        return {
            "gtk4": self.gtk4_app_type.get_active(),
            "gtk3": self.gtk3_app_type.get_active()
        }
