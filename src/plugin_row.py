
from gi.repository import Gtk, Gdk, Adw

from .constants import rootdir


@Gtk.Template(resource_path=f"{rootdir}/ui/plugin_row.ui")
class GradiencePluginRow(Adw.ActionRow):
    __gtype_name__ = "GradiencePluginRow"

    def __init__(self, name, repo, **kwargs):
        super().__init__(**kwargs)

        self.name = name
        self.set_name(name)
        self.set_title(name)
        self.set_subtitle("@" + repo)
