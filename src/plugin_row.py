
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
