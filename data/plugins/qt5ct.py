from pathlib import Path

import os

from yapsy.IPlugin import IPlugin

class Qt5ctColorScheme2Plugin(IPlugin):
    plugin_id = "qt5ct_color_scheme"
    title = "Qt5ct Color Scheme"
    author = "Gradience Team"

    def give_preset_settings(self, preset_settings, custom_settings=None):
        self.variables = preset_settings["variables"]

    def validate(self):
        return False, None

    def open_settings(self):
        return False

    def apply(self, dark_theme=False):
        def transform_color(string):
            if (string.startswith("#")):
                return '#' + 'ff' + string[1:8]
            elif (string.startswith("rgba")):
                rgba_strings = string.strip("rgba()").split(", ")
                r, g, b = [int(x) for x in rgba_strings[0:3]]
                alpha = int(float(rgba_strings[3]) * 255)
                return '#{:02x}{:02x}{:02x}{:02x}'.format(alpha, r, g, b)
            else: print("ERROR " + string)
        qt_pos = {
            "window_text":          0,
            "button_background":    1,
            "bright":               2,
            "less_bright":          3,
            "dark":                 4,
            "less_dark":            5,
            "normal_text":          6,
            "bright_text":          7,
            "button_text":          8,
            "normal_background":    9,
            "window":               10,
            "shadow":               11,
            "highlight":            12,
            "highlighted_text":     13,
            "link":                 14,
            "visited_link":         15,
            "alternate_background":	16,
            "default":              17,
            "tooltip_background":   18,
            "tooltip_text":         19,
            "placeholder_text":     20
    }
        qt_active = ["#ff000000", "#ffefefef", "#ffffffff", "#ffcacaca",
                    "#ff9f9f9f", "#ffb8b8b8", "#ff000000", "#ffffffff",
                    "#ff000000", "#ffffffff", "#ffefefef", "#ff767676",
                    "#ff308cc6", "#ffffffff", "#ff0000ff", "#ffff00ff",
                    "#fff7f7f7", "#ff000000", "#ffffffdc", "#ff000000",
                    "#80000000"]
        qt_disabled = ["#ffbebebe", "#ffefefef", "#ffffffff", "#ffcacaca",
                    "#ffbebebe", "#ffb8b8b8", "#ffbebebe", "#ffffffff",
                    "#ffbebebe", "#ffefefef", "#ffefefef", "#ffb1b1b1",
                    "#ff919191", "#ffffffff", "#ff0000ff", "#ffff00ff",
                    "#fff7f7f7", "#ff000000", "#ffffffdc", "#ff000000",
                    "#80000000"]
        qt_inactive = ["#ff000000", "#ffefefef", "#ffffffff", "#ffcacaca",
                    "#ff9f9f9f", "#ffb8b8b8", "#ff000000", "#ffffffff",
                    "#ff000000", "#ffffffff", "#ffefefef", "#ff767676",
                    "#ff308cc6", "#ffffffff", "#ff0000ff", "#ffff00ff",
                    "#fff7f7f7", "#ff000000", "#ffffffdc", "#ff000000",
                    "#80000000"]
        qt_to_gn_active = {
            "window_text":          "window_fg_color",
            "button_background":    "view_bg_color",
            #"bright":               "view_bg_color",
            #"less_bright":          "window_bg_color",
            #"bright_text":          "view_fg_color",
            "normal_text":          "popover_fg_color",
            "button_text":          "window_fg_color",
            "normal_background":    "popover_bg_color",
            "window":               "headerbar_bg_color",
            "highlight":            "accent_bg_color",
            "highlighted_text":     "accent_fg_color"
        }
        qt_to_gn_inactive = {
            "window_text":          "window_fg_color",
            "button_background":    "view_bg_color",
            "normal_text":          "popover_fg_color",
            "button_text":          "window_fg_color",
            "normal_background":    "popover_bg_color",
            "window":               "headerbar_bg_color"
        }
        qt_to_gn_disabled = {
            "button_background":    "view_bg_color",
            "window":               "window_bg_color"
        }
        qt_palettes = {
            "active_colors": qt_active,
            "disabled_colors": qt_disabled,
            "inactive_colors": qt_inactive
        }
        for gn_name, color in self.variables.items():
            matches = [k for k, v in qt_to_gn_active.items() if v == gn_name]
            if matches:
                tran = transform_color(color)
                for match in matches:
                    qt_active[qt_pos.get(match)] = tran
            matches = [k for k, v in qt_to_gn_inactive.items() if v == gn_name]
            if matches:
                tran = transform_color(color)
                for match in matches:
                    qt_inactive[qt_pos.get(match)] = tran
            matches = [k for k, v in qt_to_gn_disabled.items() if v == gn_name]
            if matches:
                tran = transform_color(color)
                for match in matches:
                    qt_disabled[qt_pos.get(match)] = tran
        try:
            path = os.path.expanduser("~/.config/qt5ct/colors")
            if not os.path.exists(path):
                os.makedirs(path)
            path = os.path.join(path, "Gradience.conf")
            print(path)
            direc = Path(path).expanduser()
            with open(direc, "w") as f:
                f.write("[ColorScheme]\n")
                for name, palette in qt_palettes.items():
                    f.write(name + "=" + ", ".join(palette) + "\n")
        except OSError:
            pass
        except StopIteration:
            pass
