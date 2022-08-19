
from gi.repository import Gtk, Gdk, Adw

from .constants import rootdir


@Gtk.Template(resource_path=f"{rootdir}/ui/plugin_row.ui")
class GradiencePluginRow(Adw.ActionRow):
    __gtype_name__ = "GradiencePluginRow"

    def __init__(self, title, id, **kwargs):
        super().__init__(**kwargs)

        self.set_name(id)
        self.set_title(title)
        self.set_subtitle("@" + id)

        switch = Gtk.Template.Child("switch")
        settings_button = Gtk.Template.Child("settings-button")
        remove_button = Gtk.Template.Child("remove-button")

    @Gtk.Template.Callback()
    def on_settings_plugin_clicked(self, *_args):
        print("settings")

    @Gtk.Template.Callback()
    def on_remove_plugin_clicked(self, *_args):
        print("removed")

    
    @Gtk.Template.Callback()
    def on_switch_toggled(self, *_args):
        print("toggled")
