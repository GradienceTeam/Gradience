from gi.repository import Gtk, Gdk, Adw

from .constants import rootdir


@Gtk.Template(resource_path=f"{rootdir}/ui/preset_row.ui")
class GradiencePresetRow(Adw.ActionRow):
    __gtype_name__ = "GradiencePresetRow"

    name_entry = Gtk.Template.Child("name_entry")
    value_stack = Gtk.Template.Child("value_stack")
    name_entry_toggle = Gtk.Template.Child("name_entry_toggle")
    apply_button = Gtk.Template.Child("apply_button")

    def __init__(self, name, author="", **kwargs):
        super().__init__(**kwargs)

        self.set_name(name)
        self.set_title(name)
        self.set_subtitle(author)

        apply_button = Gtk.Template.Child("apply_button")
        rename_button = Gtk.Template.Child("rename_button")

    @Gtk.Template.Callback()
    def on_apply_button_clicked(self, *_args):
        print("apply")

    @Gtk.Template.Callback()
    def on_name_entry_changed(self, *_args):
        self.update_value(self.name_entry.get_text(), update_from="name_entry")

    @Gtk.Template.Callback()
    def on_name_entry_toggled(self, *_args):
        if self.name_entry_toggle.get_active():
            self.value_stack.set_visible_child(self.name_entry)
        else:
            self.value_stack.set_visible_child(self.apply_button)
