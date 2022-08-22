from gi.repository import Gtk, Gdk, Adw

from .constants import rootdir


@Gtk.Template(resource_path=f"{rootdir}/ui/preset_row.ui")
class GradiencePresetRow(Adw.ActionRow):
    __gtype_name__ = "GradiencePresetRow"

    def __init__(self, name, author="", **kwargs):
        super().__init__(**kwargs)

        self.set_name(name)
        self.set_title(name)
        self.set_subtitle(author)

        apply_button = Gtk.Template.Child("apply_button")
        rename_button = Gtk.Template.Child("rename_button")

    @Gtk.Template.Callback()
    def on_rename_button_clicked(self, *_args):
        print("rename")

    @Gtk.Template.Callback()
    def on_apply_button_clicked(self, *_args):
        print("apply")
