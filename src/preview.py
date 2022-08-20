from gi.repository import Gtk, Adw, Gio, Gdk
from .constants import rootdir

@Gtk.Template(resource_path=f"{rootdir}/ui/preview.ui")
class GradiencePreviewWindow(Adw.Window):
    __gtype_name__ = "GradiencePreviewWindow"

    def __init__(self, window, **kwargs) -> None:
        super().__init__(**kwargs)

        self.window = window

        