from pathlib import Path
import os
import shutil
from ..constants import data_dir
from .utils import to_slug_case
import subprocess
THEME_DIR = Path(data_dir) / "themes"
USER_THEME_DIR = Path("~/.themes").expanduser()
USER_THEME_DIR.mkdir(parents=True, exist_ok=True)

ADW_GTK3_DIR = THEME_DIR / "adw-gtk3" / "gtk-3.0"
ADW_GTK3_CSS = ADW_GTK3_DIR / "gtk.css"
ADW_GTK3_CSS_DARK = ADW_GTK3_DIR / "gtk-dark.css"
ADW_GTK3_ASSETS_DIR = ADW_GTK3_DIR / "assets"

ADW_GTK3_TO_REPLACE = """@define-color blue_1 #99c1f1;
@define-color blue_2 #62a0ea;
@define-color blue_3 #3584e4;
@define-color blue_4 #1c71d8;
@define-color blue_5 #1a5fb4;
@define-color green_1 #8ff0a4;
@define-color green_2 #57e389;
@define-color green_3 #33d17a;
@define-color green_4 #2ec27e;
@define-color green_5 #26a269;
@define-color yellow_1 #f9f06b;
@define-color yellow_2 #f8e45c;
@define-color yellow_3 #f6d32d;
@define-color yellow_4 #f5c211;
@define-color yellow_5 #e5a50a;
@define-color orange_1 #ffbe6f;
@define-color orange_2 #ffa348;
@define-color orange_3 #ff7800;
@define-color orange_4 #e66100;
@define-color orange_5 #c64600;
@define-color red_1 #f66151;
@define-color red_2 #ed333b;
@define-color red_3 #e01b24;
@define-color red_4 #c01c28;
@define-color red_5 #a51d2d;
@define-color purple_1 #dc8add;
@define-color purple_2 #c061cb;
@define-color purple_3 #9141ac;
@define-color purple_4 #813d9c;
@define-color purple_5 #613583;
@define-color brown_1 #cdab8f;
@define-color brown_2 #b5835a;
@define-color brown_3 #986a44;
@define-color brown_4 #865e3c;
@define-color brown_5 #63452c;
@define-color light_1 #ffffff;
@define-color light_2 #f6f5f4;
@define-color light_3 #deddda;
@define-color light_4 #c0bfbc;
@define-color light_5 #9a9996;
@define-color dark_1 #77767b;
@define-color dark_2 #5e5c64;
@define-color dark_3 #3d3846;
@define-color dark_4 #241f31;
@define-color dark_5 #000000;
@define-color accent_bg_color @blue_3;
@define-color accent_fg_color white;
@define-color accent_color @blue_4;
@define-color destructive_bg_color @red_3;
@define-color destructive_fg_color white;
@define-color destructive_color @red_4;
@define-color success_bg_color @green_4;
@define-color success_fg_color white;
@define-color success_color @green_5;
@define-color warning_bg_color @yellow_5;
@define-color warning_fg_color rgba(0, 0, 0, 0.8);
@define-color warning_color #ae7b03;
@define-color error_bg_color @red_3;
@define-color error_fg_color white;
@define-color error_color @red_4;
@define-color window_bg_color #fafafa;
@define-color window_fg_color #323232;
@define-color view_bg_color #ffffff;
@define-color view_fg_color #000000;
@define-color headerbar_bg_color #ebebeb;
@define-color headerbar_fg_color #2f2f2f;
@define-color headerbar_border_color rgba(0, 0, 0, 0.8);
@define-color headerbar_backdrop_color @window_bg_color;
@define-color headerbar_shade_color rgba(0, 0, 0, 0.07);
@define-color card_bg_color #ffffff;
@define-color card_fg_color #333333;
@define-color card_shade_color rgba(0, 0, 0, 0.07);
@define-color dialog_bg_color #fafafa;
@define-color dialog_fg_color #323232;
@define-color popover_bg_color #ffffff;
@define-color popover_fg_color #333333;
@define-color thumbnail_bg_color #ffffff;
@define-color thumbnail_fg_color rgba(0, 0, 0, 0.8);
@define-color shade_color rgba(0, 0, 0, 0.07);
@define-color scrollbar_outline_color white;"""

ADW_GTK3_TO_REPLACE_DARK = """@define-color blue_1 #99c1f1;
@define-color blue_2 #62a0ea;
@define-color blue_3 #3584e4;
@define-color blue_4 #1c71d8;
@define-color blue_5 #1a5fb4;
@define-color green_1 #8ff0a4;
@define-color green_2 #57e389;
@define-color green_3 #33d17a;
@define-color green_4 #2ec27e;
@define-color green_5 #26a269;
@define-color yellow_1 #f9f06b;
@define-color yellow_2 #f8e45c;
@define-color yellow_3 #f6d32d;
@define-color yellow_4 #f5c211;
@define-color yellow_5 #e5a50a;
@define-color orange_1 #ffbe6f;
@define-color orange_2 #ffa348;
@define-color orange_3 #ff7800;
@define-color orange_4 #e66100;
@define-color orange_5 #c64600;
@define-color red_1 #f66151;
@define-color red_2 #ed333b;
@define-color red_3 #e01b24;
@define-color red_4 #c01c28;
@define-color red_5 #a51d2d;
@define-color purple_1 #dc8add;
@define-color purple_2 #c061cb;
@define-color purple_3 #9141ac;
@define-color purple_4 #813d9c;
@define-color purple_5 #613583;
@define-color brown_1 #cdab8f;
@define-color brown_2 #b5835a;
@define-color brown_3 #986a44;
@define-color brown_4 #865e3c;
@define-color brown_5 #63452c;
@define-color light_1 #ffffff;
@define-color light_2 #f6f5f4;
@define-color light_3 #deddda;
@define-color light_4 #c0bfbc;
@define-color light_5 #9a9996;
@define-color dark_1 #77767b;
@define-color dark_2 #5e5c64;
@define-color dark_3 #3d3846;
@define-color dark_4 #241f31;
@define-color dark_5 #000000;
@define-color accent_bg_color @blue_3;
@define-color accent_fg_color white;
@define-color accent_color #78aeed;
@define-color destructive_bg_color @red_4;
@define-color destructive_fg_color white;
@define-color destructive_color #ff7b63;
@define-color success_bg_color @green_5;
@define-color success_fg_color white;
@define-color success_color @green_1;
@define-color warning_bg_color #cd9309;
@define-color warning_fg_color rgba(0, 0, 0, 0.8);
@define-color warning_color @yellow_2;
@define-color error_bg_color @red_4;
@define-color error_fg_color white;
@define-color error_color #ff7b63;
@define-color window_bg_color #242424;
@define-color window_fg_color white;
@define-color view_bg_color #1e1e1e;
@define-color view_fg_color #ffffff;
@define-color headerbar_bg_color #303030;
@define-color headerbar_fg_color white;
@define-color headerbar_border_color white;
@define-color headerbar_backdrop_color @window_bg_color;
@define-color headerbar_shade_color rgba(0, 0, 0, 0.36);
@define-color card_bg_color rgba(255, 255, 255, 0.08);
@define-color card_fg_color white;
@define-color card_shade_color rgba(0, 0, 0, 0.36);
@define-color dialog_bg_color #383838;
@define-color dialog_fg_color white;
@define-color popover_bg_color #383838;
@define-color popover_fg_color white;
@define-color thumbnail_bg_color #383838;
@define-color thumbnail_fg_color white;
@define-color shade_color rgba(0, 0, 0, 0.36);
@define-color scrollbar_outline_color rgba(0, 0, 0, 0.5);"""

class Theme:
    def __init__(
        self,
        name,
        preset,
        icon_theme="Adwaita",
        comment="A theme generated by Gradience",
        cursor_theme="Adwaita",
        button_layout="close,minimize,maximize:menu",
    ) -> None:
        self.name = name
        self.dir_name = to_slug_case(name)
        self.path = Path("~/.themes").expanduser() / self.dir_name
        if not self.path.exists():
            self.path.mkdir(parents=True)
        self.preset = preset

        self.icon_theme = icon_theme
        self.cursor_theme = cursor_theme
        self.button_layout = button_layout
        self.comment = comment

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"Theme({self.name})"

    def create(self):
        shutil.rmtree(self.path)
        self.create_gtk3()
        self.create_gtk4()
        self.create_gnome_shell()
        self.create_index()
        self.apply_theme()

    def create_gtk3(self):
        gtk3_path = self.path / "gtk-3.0"
        if not gtk3_path.exists():
            gtk3_path.mkdir(parents=True)

        shutil.copytree(ADW_GTK3_ASSETS_DIR, gtk3_path / "assets")

        self.create_gtk3_dark()
        self.create_gtk3_light()

    def create_gtk3_dark(self):
        gtk3_dark_path = self.path / "gtk-3.0" / "gtk-dark.css"
        shutil.copy(ADW_GTK3_CSS_DARK, gtk3_dark_path)
        with (open(ADW_GTK3_CSS_DARK, "r", encoding="utf-8") as original,
              open(gtk3_dark_path, "w", encoding="utf-8") as modified):
            modified.write(original.read().replace(ADW_GTK3_TO_REPLACE_DARK, self.preset.dark.to_css("gtk3")))

    def create_gtk3_light(self):
        gtk3_light_path = self.path / "gtk-3.0" / "gtk.css"
        shutil.copy(ADW_GTK3_CSS, gtk3_light_path)
        with (open(ADW_GTK3_CSS, "r", encoding="utf-8") as original,
              open(gtk3_light_path, "w", encoding="utf-8") as modified):
            modified.write(original.read().replace(ADW_GTK3_TO_REPLACE, self.preset.light.to_css("gtk3")))

    def create_gtk4(self):
        gtk4_path = self.path / "gtk-4.0"
        if not gtk4_path.exists():
            gtk4_path.mkdir(parents=True)

        self.create_gtk4_dark()
        self.create_gtk4_light()

        config_path = Path("~/.config/gtk-4.0").expanduser()
        try:
            shutil.rmtree(config_path)
        except OSError:
            os.remove(config_path)
        os.symlink(gtk4_path, Path("~/.config/gtk-4.0").expanduser())

    def create_gtk4_dark(self):
        gtk4_dark_path = self.path / "gtk-4.0" / "gtk-dark.css"
        with open(gtk4_dark_path, "w", encoding="utf-8") as f:
            f.write(self.preset.dark.to_css("gtk4"))

    def create_gtk4_light(self):
        gtk4_light_path = self.path / "gtk-4.0" / "gtk.css"
        with open(gtk4_light_path, "w", encoding="utf-8") as f:
            f.write(self.preset.light.to_css("gtk4"))

    def create_gnome_shell(self):
        pass

    def apply_theme(self):
        subprocess.run(["gsettings", "set", "org.gnome.desktop.interface", "gtk-theme", self.name])

    def create_index(self, *args, **kwargs):
        index_theme = self.path / "index.theme"
        name = kwargs.get("name", self.name)
        comment = kwargs.get("comment", self.comment)
        icon_theme = kwargs.get("icon-theme", self.icon_theme)
        cursor_theme = kwargs.get("cursor-theme", self.cursor_theme)
        button_layout = kwargs.get("button-layout", self.button_layout)

        with index_theme.open("w") as f:
            f.write(
                """
[Desktop Entry]
Type=X-GNOME-Metatheme
Name={name}
Comment={comment}
Encoding=UTF-8

[X-GNOME-Metatheme]
GtkTheme={name}
IconTheme={icon_theme}
CursorTheme={cursor_theme}
ButtonLayout={button_layout}

""".format(
                    name=name,
                    comment=comment,
                    icon_theme=icon_theme,
                    cursor_theme=cursor_theme,
                    button_layout=button_layout,
                )
            )
