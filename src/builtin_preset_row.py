from gi.repository import Gtk, Gdk, Adw

from .constants import rootdir
from .modules.utils import to_slug_case, buglog
import json
import os


@Gtk.Template(resource_path=f"{rootdir}/ui/builtin_preset_row.ui")
class GradienceBuiltinPresetRow(Adw.ActionRow):
    __gtype_name__ = "GradienceBuiltinPresetRow"

    apply_button = Gtk.Template.Child("apply_button")

    def __init__(self, name, toast_overlay, author="", **kwargs):
        super().__init__(**kwargs)

        self.name = name

        self.set_name(name)
        self.set_title(name)
        self.set_subtitle(author)

        self.app = Gtk.Application.get_default()

        self.toast_overlay = toast_overlay

        apply_button = Gtk.Template.Child("apply_button")

    @Gtk.Template.Callback()
    def on_apply_button_clicked(self, *_args):
        buglog("apply")

        self.app.load_preset_from_resource(
            f"{rootdir}/presets/"
            + to_slug_case(self.name) + ".json"
        )
