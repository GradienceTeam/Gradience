from pathlib import Path
from configparser import ConfigParser
import os

from yapsy.IPlugin import IPlugin

TEMPLATE = """
/*
 * =================================================================================== *
 * This file was overwritten by the mailspring_libadwaita_theme plugin from Gradience  *
 *                                                                                     *
 * Report issue at: https://github.com/GradienceTeam/Plugins/issues/new/choose         *
 * Join us on matrix: https://matrix.to/#/#Gradience:matrix.org                        *
 * =================================================================================== *
 */

//------------------------------------------------------------
// Asset path
//------------------------------------------------------------

@asset_path: "Libadwaita";

//------------------------------------------------------------
// Variant colors (light/dark)
//------------------------------------------------------------

// Text color
@text_color: {card_fg_color};

// Accent colors
@accent_bg_color: {accent_bg_color};
@accent_fg_color: {accent_fg_color};
@accent_color: {accent_color};

// Success colors
@success_bg_color: {success_bg_color};
@success_fg_color: {success_fg_color};
@success_color: {success_color};

// Warning colors
@warning_color: {warning_color};
@warning_bg_color: {warning_bg_color};
@warning_fg_color: {warning_fg_color};

// Error colors
@error_color: {error_color};
@error_bg_color: {error_bg_color};
@error_fg_color: {error_fg_color};

// Window/header colors
@window_bg_color: {window_bg_color};
@headerbar_bg_color: {headerbar_bg_color};

// Card colors
@card_bg_color: {card_bg_color};

// Popover colors
@popover_bg_color: {popover_bg_color};

// View colors
@view_bg_color: {view_bg_color};
@view_fg_color: {view_fg_color};

// Scrollbar colors
@scrollbar_outline_color: {scrollbar_outline_color};

//------------------------------------------------------------
// User variables
//------------------------------------------------------------

// Text size
@text_size: 15px;

// Control height (button/input/select)
@button_height: 34px;

// Popover item height
@popover_item_height: 32px;

//------------------------------------------------------------
// Palette colors (fixed)
//------------------------------------------------------------
@yellow_4: #f5c211;

//------------------------------------------------------------
// Calculated + fixed colors (do not modify)
//------------------------------------------------------------

// Dim text color
@text_color_dim: fade(@text_color, alpha(@text_color)*100*0.55);

// Border color
@borders_color: fade(@text_color, alpha(@text_color)*100*0.15);

// Focus border color
@focus_border_color: fade(@accent_color, 50%);

// View colors
@view_hover_color: fade(@text_color, alpha(@text_color)*100*0.07);
@view_active_color: fade(@text_color, alpha(@text_color)*100*0.16);
@view_selected_color: fade(@text_color, alpha(@text_color)*100*0.1);
@view_selected_hover_color: fade(@text_color, alpha(@text_color)*100*0.13);
@view_selected_active_color: fade(@text_color, alpha(@text_color)*100*0.19);

// Button colors
@button_color: fade(@text_color, alpha(@text_color)*100*0.1);
@button_hover_color: fade(@text_color, alpha(@text_color)*100*0.15);
@button_active_color: fade(@text_color, alpha(@text_color)*100*0.3);
@button_checked_color: fade(@text_color, alpha(@text_color)*100*0.3);
@button_checked_hover_color: fade(@text_color, alpha(@text_color)*100*0.35);

// Default button colors
@button_default_hover_color: linear-gradient(fade(@text_color, alpha(@text_color)*100*0.1), fade(@text_color, alpha(@text_color)*100*0.1));
@button_default_active_color: linear-gradient(fade(black, 20%), fade(black, 20%));

// Trough colors (used for checkboxes and radio buttons)
@trough_color: fade(@text_color, alpha(@text_color)*100*0.15);
@trough_hover_color: fade(@text_color, alpha(@text_color)*100*0.2);
@trough_active_color: fade(@text_color, alpha(@text_color)*100*0.25);

// Checkbox/radio button colors
@check_shadow: inset 0 0 0 2px @trough_color;
@check_hover_shadow: inset 0 0 0 2px @trough_hover_color;
@check_active_color: @trough_active_color;
@check_selected_hover_color: linear-gradient(fade(@accent_fg_color, 10%), fade(@accent_fg_color, 10%));
@check_selected_active_color: linear-gradient(fade(black, 20%), fade(black, 20%));

// Card colors
@card_shadow: 0 0 0 1px fade(black, 3%), 0 1px 3px 1px fade(black, 7%), 0 2px 6px 2px fade(black, 3%);

// Popover colors
@popover_border_color: fade(black, 14%);
@popover_shadow: 0 1px 5px 1px fade(black, 9%), 0 2px 14px 3px fade(black, 5%);

// OSD colors
@osd_bg_color: fade(black, 70%);
@osd_fg_color: fade(white, 90%);
@osd_button_color: fade(white, 9%);
@osd_button_hover_color: fade(white, 13.5%);

// Link colors
@link_color: @accent_color;
@link_hover_color: mix(@accent_color, @view_fg_color, 80%);

// Scale slider colors
@slider_color: mix(white, @view_bg_color, 80%);
@slider_shadow: 0 2px 4px fade(black, 20%);
@slider_outline: 1px solid fade(black, 10%);
@slider_hover_color: white;

// Tooltip colors
@tooltip_bg_color: fade(black, 80%);
@tooltip_fg_color: white;
@tooltip_border_color: fade(white, 10%);

// Scrollbar colors
@scrollbar_track_color: fade(@text_color, alpha(@text_color)*100*0.1);
@scrollbar_slider_color: fade(@text_color, alpha(@text_color)*100*0.2);
@scrollbar_slider_hover_color: fade(@text_color, alpha(@text_color)*100*0.4);
@scrollbar_slider_dragging_color: fade(@text_color, alpha(@text_color)*100*0.6);

//------------------------------------------------------------
// Other fixed variables
//------------------------------------------------------------

// Disabled opacity
@disabled_opacity: 0.5;

// Button radius
@button_radius: 6px;

// Card radius
@card_radius: 12px;

// Popover radius
@popover_radius: 12px;

"""


class MailspringPlugin(IPlugin):
    plugin_id = "mailspring_libadwaita_theme"
    title = "Mailspring Libadwaita Theme"
    author = "Spaziale"
    template = TEMPLATE

    def give_preset_settings(self, preset_settings, custom_settings=None):
        self.variables = preset_settings["variables"]

    def validate(self):
        return False, None

    def open_settings(self):
        return False

    def apply(self, dark_theme=False):
        for path in [
            "~/.config/Mailspring/packages/Libadwaita/styles",
            "~/.var/app/com.getmailspring.Mailspring/config/Mailspring/packages/Libadwaita/styles"
        ]:
            directory = os.path.expanduser(path)
            if not os.path.exists(directory):
                os.makedirs(directory)

            try:
                with open(
                    f"{directory}/main.less",
                    "w",
                ) as f:
                    f.write(self.template.format(**self.variables))
            except OSError:
                pass
            except StopIteration:
                pass
