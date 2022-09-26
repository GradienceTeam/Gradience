from gi.repository import Gtk, Adw

from .constants import rootdir


@Gtk.Template(resource_path=f"{rootdir}/ui/no_plugin_pref.ui")
class GradienceNoPluginPrefWindow(Adw.Window):
    __gtype_name__ = "GradienceNoPluginPrefWindow"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
