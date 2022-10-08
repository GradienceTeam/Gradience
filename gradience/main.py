# main.py
#
# Change the look of Adwaita, with ease
# Copyright (C) 2022 Gradience Team
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

import sys
import json
import os
import threading

from pathlib import Path
from material_color_utilities_python import *

from gi.repository import Gtk, Gdk, Gio, Adw, GLib, Xdp, XdpGtk4

from .settings_schema import settings_schema
from .window import GradienceMainWindow
from .app_type_dialog import GradienceAppTypeDialog
from .custom_css_group import GradienceCustomCSSGroup
from .constants import (
    rootdir,
    app_id,
    rel_ver,
    version,
    bugtracker_url,
    help_url,
    project_url,
)
from .modules.css import load_preset_from_css
from .welcome import GradienceWelcomeWindow
from .preferences import GradiencePreferencesWindow
from .modules.utils import to_slug_case, buglog, run_command
from .plugins_list import GradiencePluginsList
from .presets_manager_window import GradiencePresetWindow
from .modules.preset import Preset, presets_dir


class GradienceApplication(Adw.Application):
    """The main application singleton class."""

    __gtype_name__ = "GradienceApplication"

    settings = Gio.Settings.new(app_id)

    def __init__(self):
        super().__init__(application_id=app_id, flags=Gio.ApplicationFlags.FLAGS_NONE)
        self.set_resource_base_path(rootdir)

        self.portal = Xdp.Portal()

        self.preset_name = ""
        self.is_dirty = False

        self.variables = {}
        self.pref_variables = {}

        self.palette = {}
        self.pref_palette_shades = {}

        self.custom_css = {}
        self.custom_css_group = None

        self.custom_presets = {}
        self.global_errors = []
        self.current_css_provider = None

        self.is_ready = False

        self.first_run = self.settings.get_boolean("first-run")
        self.last_opened_version = self.settings.get_string(
            "last-opened-version")

        self.favourite = set(self.settings.get_value("favourite"))

        self.style_manager = Adw.StyleManager.get_default()

        self.preset = None

    def do_activate(self):
        """Called when the application is activated.

        We raise the application's main window, creating it if
        necessary.
        """

        self.win = self.props.active_window
        if not self.win:
            self.win = GradienceMainWindow(
                application=self,
                default_height=self.settings.get_int("window-height"),
                default_width=self.settings.get_int("window-width"),
                fullscreened=self.settings.get_boolean("window-fullscreen"),
                maximized=self.settings.get_boolean("window-maximized"),
            )
        self.plugins_list = GradiencePluginsList(self.win)
        self.setup_plugins()

        self.create_action("open_preset_directory", self.open_preset_directory)
        self.create_stateful_action(
            "load_preset",
            GLib.VariantType.new("s"),
            GLib.Variant("s", "adwaita"),
            self.load_preset_action,
        )
        self.create_action("apply_color_scheme",
                           self.show_apply_color_scheme_dialog)

        self.create_action("show_adwaita_demo", self.show_adwaita_demo)

        self.create_action("show_gtk4_widget_factory",
                           self.show_gtk4_widget_factory)

        self.create_action("show_gtk4_demo", self.show_gtk4_demo)

        self.create_action(
            "restore_color_scheme", self.show_restore_color_scheme_dialog
        )
        self.create_action("manage_presets", self.show_presets_manager)

        self.create_action("reset_color_scheme",
                           self.show_reset_color_scheme_dialog)
        self.create_action("preferences", self.show_preferences)
        self.create_action("save_preset", self.show_save_preset_dialog)
        self.create_action("about", self.show_about_window)
        self.load_preset_from_css()

        self.reload_user_defined_presets()

        if self.first_run:
            welcome = GradienceWelcomeWindow(self.win)
            welcome.present()
        else:
            if rel_ver != self.last_opened_version:
                welcome = GradienceWelcomeWindow(self.win, update=True)
                welcome.present()
            else:
                buglog("normal run")
                self.win.present()

    def save_favourite(self):
        self.settings.set_value(
            "favourite", GLib.Variant("as", self.favourite))

    def reload_user_defined_presets(self):
        if self.props.active_window.presets_menu.get_n_items() > 1:
            self.props.active_window.presets_menu.remove(1)

        if not os.path.exists(presets_dir):
            os.makedirs(presets_dir)

        self.custom_presets = {"user": {}}
        for repo in Path(presets_dir).iterdir():
            if repo.is_dir():  # repo
                presets_list = {}
                for file_name in repo.iterdir():
                    file_name = str(file_name)
                    if file_name.endswith(".json"):
                        try:
                            with open(
                                os.path.join(presets_dir, file_name),
                                "r",
                                encoding="utf-8",
                            ) as file:
                                preset_text = file.read()
                            preset = json.loads(preset_text)
                            if preset.get("variables") is None:
                                raise KeyError("variables")
                            if preset.get("palette") is None:
                                raise KeyError("palette")
                            presets_list[file_name.replace(".json", "")] = preset[
                                "name"
                            ]
                        except Exception:
                            self.win.toast_overlay.add_toast(
                                Adw.Toast(title=_("Failed to load preset"))
                            )

                self.custom_presets[repo.name] = presets_list
            elif repo.is_file():
                buglog("file")
                # keep compatiblity with old presets
                if repo.name.endswith(".json"):
                    if not os.path.isdir(os.path.join(presets_dir, "user")):
                        os.mkdir(os.path.join(presets_dir, "user"))

                    os.rename(repo, os.path.join(
                        presets_dir, "user", repo.name))

                    try:
                        with open(
                            os.path.join(presets_dir, "user", repo),
                            "r",
                            encoding="utf-8",
                        ) as file:
                            preset_text = file.read()
                        preset = json.loads(preset_text)
                        if preset.get("variables") is None:
                            raise KeyError("variables")
                        if preset.get("palette") is None:
                            raise KeyError("palette")
                        presets_list["user"][file_name.replace(".json", "")] = preset[
                            "name"
                        ]
                    except Exception:
                        self.win.toast_overlay.add_toast(
                            Adw.Toast(title=_("Failed to load preset"))
                        )

                    buglog(self.custom_presets)
        custom_menu_section = Gio.Menu()
        try:
            if (
                self.custom_presets["user"]
                or self.custom_presets["curated"]
                or self.custom_presets["official"]
            ):
                for repo, content in self.custom_presets.items():

                    for preset, preset_name in content.items():
                        buglog(preset_name)
                        if preset_name in self.favourite:
                            menu_item = Gio.MenuItem()
                            menu_item.set_label(preset_name)
                            if not preset.startswith("error"):
                                menu_item.set_action_and_target_value(
                                    "app.load_preset",
                                    GLib.Variant("s", "custom-" + preset),
                                )
                            else:
                                menu_item.set_action_and_target_value("")
                            custom_menu_section.append_item(menu_item)
            else:
                menu_item = Gio.MenuItem()
                menu_item.set_label(_("No presets found"))
                custom_menu_section.append_item(menu_item)

        except KeyError:
            if not os.path.exists(os.path.join(presets_dir, "user")):
                os.makedirs(os.path.join(presets_dir, "user"))
            if not os.path.exists(os.path.join(presets_dir, "curated")):
                os.makedirs(os.path.join(presets_dir, "curated"))
            if not os.path.exists(os.path.join(presets_dir, "official")):
                os.makedirs(os.path.join(presets_dir, "official"))
        open_in_file_manager_item = Gio.MenuItem()
        open_in_file_manager_item.set_label(_("Open in File Manager"))
        open_in_file_manager_item.set_action_and_target_value(
            "app.open_preset_directory"
        )

        # custom_menu_section.append_item(open_in_file_manager_item)
        self.props.active_window.presets_menu.append_section(
            _("Favourite Presets"), custom_menu_section
        )

    def show_presets_manager(self, *args):
        presets = GradiencePresetWindow(self)
        presets.set_transient_for(self.win)
        presets.set_modal(True)
        presets.present()

        add_rows_thread = threading.Thread(target=presets.add_explore_rows)
        add_rows_thread.start()

    def load_preset_from_css(self):
        try:
            variables, palette, custom_css = load_preset_from_css(
                os.path.join(
                    os.environ.get("XDG_CONFIG_HOME",
                                   os.environ["HOME"] + "/.config"),
                    "gtk-4.0",
                    "gtk.css",
                )
            )
            preset = {
                "name": "User",
                "variables": variables,
                "palette": palette,
                "custom_css": {"gtk4": custom_css},
            }
            self.preset = Preset(preset=preset)
            self.load_preset_variables_from_preset()
        except OSError:  # fallback to adwaita
            if self.style_manager.get_dark():
                self.load_preset_from_resource(
                    f"{rootdir}/presets/adwaita-dark.json")
            else:
                self.load_preset_from_resource(
                    f"{rootdir}/presets/adwaita.json")

    def open_preset_directory(self, *_args):
        parent = XdpGtk4.parent_new_gtk(self.props.active_window)

        def open_dir_callback(_, result):
            self.portal.open_uri_finish(result)

        self.portal.open_uri(
            parent,
            "file://"
            + os.path.join(
                os.environ.get("XDG_CONFIG_HOME",
                               os.environ["HOME"] + "/.config"),
                "presets",
            ),
            Xdp.OpenUriFlags.NONE,
            None,
            open_dir_callback,
        )

    def load_preset_from_file(self, preset_path):
        buglog(f"load preset from file {preset_path}")
        self.preset = Preset(preset_path=preset_path)
        self.load_preset_variables_from_preset()

    def load_preset_from_resource(self, preset_path):
        preset_text = Gio.resources_lookup_data(
            preset_path, 0).get_data().decode()
        self.preset = Preset(text=preset_text)
        self.load_preset_variables_from_preset()

    def load_preset_variables_from_preset(self, preset=None):
        if preset is not None:
            self.preset = preset
        self.is_ready = False
        buglog(self.preset)
        self.preset_name = self.preset.preset_name
        self.variables = self.preset.variables
        self.palette = self.preset.palette
        self.custom_css = self.preset.custom_css

        for key in self.variables.keys():
            if key in self.pref_variables:
                self.pref_variables[key].update_value(self.variables[key])
        for key in self.palette.keys():
            if key in self.pref_palette_shades:
                self.pref_palette_shades[key].update_shades(self.palette[key])
        self.custom_css_group.load_custom_css(self.custom_css)

        self.clear_dirty()

        self.reload_variables()

    def load_preset_variables(self, preset):
        self.is_ready = False

        self.preset_name = preset["name"]
        self.variables = preset["variables"]
        self.palette = preset["palette"]
        if "custom_css" in preset:
            self.custom_css = preset["custom_css"]
        else:
            for app_type in settings_schema["custom_css_app_types"]:
                self.custom_css[app_type] = ""
        for key in self.variables.keys():
            if key in self.pref_variables:
                self.pref_variables[key].update_value(self.variables[key])
        for key in self.palette.keys():
            if key in self.pref_palette_shades:
                self.pref_palette_shades[key].update_shades(self.palette[key])
        self.custom_css_group.load_custom_css(self.custom_css)

        self.clear_dirty()

        self.reload_variables()

    @staticmethod
    def rgba_from_argb(argb, alpha=None) -> str:
        base = "rgba({}, {}, {}, {})"

        red = redFromArgb(argb)
        green = greenFromArgb(argb)
        blue = blueFromArgb(argb)
        if not alpha:
            alpha = alphaFromArgb(argb)

        return base.format(red, green, blue, alpha)

    def update_theme_from_monet(self, theme, tone, monet_theme):
        palettes = theme["palettes"]

        monet_theme = monet_theme.get_string().lower()  # dark / light

        palette = {}
        i = 0
        for color in palettes.values():
            i += 1
            palette[str(i)] = hexFromArgb(color.tone(int(tone.get_string())))
        self.pref_palette_shades["monet"].update_shades(palette)
        if monet_theme == "auto":
            if self.style_manager.get_dark():
                monet_theme = "dark"
            else:
                monet_theme = "light"

        if monet_theme == "dark":
            dark_theme = theme["schemes"]["dark"]
            variable = {
                "accent_color": self.rgba_from_argb(dark_theme.primary),
                "accent_bg_color": self.rgba_from_argb(dark_theme.primaryContainer),
                "accent_fg_color": self.rgba_from_argb(dark_theme.onPrimaryContainer),
                "destructive_color": self.rgba_from_argb(dark_theme.error),
                "destructive_bg_color": self.rgba_from_argb(dark_theme.errorContainer),
                "destructive_fg_color": self.rgba_from_argb(
                    dark_theme.onErrorContainer
                ),
                "success_color": self.rgba_from_argb(dark_theme.tertiary),
                "success_bg_color": self.rgba_from_argb(dark_theme.onTertiary),
                "success_fg_color": self.rgba_from_argb(dark_theme.onTertiaryContainer),
                "warning_color": self.rgba_from_argb(dark_theme.secondary),
                "warning_bg_color": self.rgba_from_argb(dark_theme.onSecondary),
                "warning_fg_color": self.rgba_from_argb(dark_theme.primary, "0.8"),
                "error_color": self.rgba_from_argb(dark_theme.error),
                "error_bg_color": self.rgba_from_argb(dark_theme.errorContainer),
                "error_fg_color": self.rgba_from_argb(dark_theme.onError),
                "window_bg_color": self.rgba_from_argb(dark_theme.surface),
                "window_fg_color": self.rgba_from_argb(dark_theme.onSurface),
                "view_bg_color": self.rgba_from_argb(dark_theme.surface),
                "view_fg_color": self.rgba_from_argb(dark_theme.onSurface),
                "headerbar_bg_color": self.rgba_from_argb(dark_theme.surface),
                "headerbar_fg_color": self.rgba_from_argb(dark_theme.onSurface),
                "headerbar_border_color": self.rgba_from_argb(
                    dark_theme.primary, "0.8"
                ),
                "headerbar_backdrop_color": "@headerbar_bg_color",
                "headerbar_shade_color": self.rgba_from_argb(dark_theme.shadow),
                "card_bg_color": self.rgba_from_argb(dark_theme.primary, "0.05"),
                "card_fg_color": self.rgba_from_argb(dark_theme.onSecondaryContainer),
                "card_shade_color": self.rgba_from_argb(dark_theme.shadow),
                "dialog_bg_color": self.rgba_from_argb(dark_theme.secondaryContainer),
                "dialog_fg_color": self.rgba_from_argb(dark_theme.onSecondaryContainer),
                "popover_bg_color": self.rgba_from_argb(dark_theme.secondaryContainer),
                "popover_fg_color": self.rgba_from_argb(
                    dark_theme.onSecondaryContainer
                ),
                "shade_color": self.rgba_from_argb(dark_theme.shadow),
                "scrollbar_outline_color": self.rgba_from_argb(dark_theme.outline),
            }
        else:  # light
            light_theme = theme["schemes"]["light"]
            variable = {
                "accent_color": self.rgba_from_argb(light_theme.primary),
                "accent_bg_color": self.rgba_from_argb(light_theme.primary),
                "accent_fg_color": self.rgba_from_argb(light_theme.onPrimary),
                "destructive_color": self.rgba_from_argb(light_theme.error),
                "destructive_bg_color": self.rgba_from_argb(light_theme.errorContainer),
                "destructive_fg_color": self.rgba_from_argb(
                    light_theme.onErrorContainer
                ),
                "success_color": self.rgba_from_argb(light_theme.tertiary),
                "success_bg_color": self.rgba_from_argb(light_theme.tertiaryContainer),
                "success_fg_color": self.rgba_from_argb(
                    light_theme.onTertiaryContainer
                ),
                "warning_color": self.rgba_from_argb(light_theme.secondary),
                "warning_bg_color": self.rgba_from_argb(light_theme.secondaryContainer),
                "warning_fg_color": self.rgba_from_argb(
                    light_theme.onSecondaryContainer
                ),
                "error_color": self.rgba_from_argb(light_theme.error),
                "error_bg_color": self.rgba_from_argb(light_theme.errorContainer),
                "error_fg_color": self.rgba_from_argb(light_theme.onError),
                "window_bg_color": self.rgba_from_argb(light_theme.secondaryContainer),
                "window_fg_color": self.rgba_from_argb(light_theme.onSurface),
                "view_bg_color": self.rgba_from_argb(light_theme.secondaryContainer),
                "view_fg_color": self.rgba_from_argb(light_theme.onSurface),
                "headerbar_bg_color": self.rgba_from_argb(
                    light_theme.secondaryContainer
                ),
                "headerbar_fg_color": self.rgba_from_argb(light_theme.onSurface),
                "headerbar_border_color": self.rgba_from_argb(
                    light_theme.primary, "0.8"
                ),
                "headerbar_backdrop_color": "@headerbar_bg_color",
                "headerbar_shade_color": self.rgba_from_argb(
                    light_theme.secondaryContainer
                ),
                "card_bg_color": self.rgba_from_argb(light_theme.primary, "0.05"),
                "card_fg_color": self.rgba_from_argb(light_theme.onSecondaryContainer),
                "card_shade_color": self.rgba_from_argb(light_theme.shadow),
                "dialog_bg_color": self.rgba_from_argb(light_theme.secondaryContainer),
                "dialog_fg_color": self.rgba_from_argb(
                    light_theme.onSecondaryContainer
                ),
                "popover_bg_color": self.rgba_from_argb(light_theme.secondaryContainer),
                "popover_fg_color": self.rgba_from_argb(
                    light_theme.onSecondaryContainer
                ),
                "shade_color": self.rgba_from_argb(light_theme.shadow),
                "scrollbar_outline_color": self.rgba_from_argb(light_theme.outline),
            }

        for key in variable:
            if key in self.pref_variables:
                self.pref_variables[key].update_value(variable[key])

        self.reload_variables()

    def generate_gtk_css(self, app_type):
        final_css = ""
        for key in self.variables.keys():
            final_css += f"@define-color {key} {self.variables[key]};\n"
        for prefix_key in self.palette.keys():
            for key in self.palette[prefix_key].keys():
                final_css += f"@define-color {prefix_key + key} {self.palette[prefix_key][key]};\n"
        final_css += self.custom_css.get(app_type, "")
        return final_css

    def mark_as_dirty(self):
        self.is_dirty = True
        self.props.active_window.save_preset_button.get_child().set_icon_name(
            "drive-unsaved-symbolic"
        )
        self.props.active_window.save_preset_button.add_css_class("warning")

        self.props.active_window.save_preset_button.get_child().set_tooltip_text(
            _("Unsaved Changes")
        )

    def clear_dirty(self):
        self.is_dirty = False
        self.props.active_window.save_preset_button.get_child().set_icon_name(
            "drive-symbolic"
        )
        self.props.active_window.save_preset_button.remove_css_class("warning")
        self.props.active_window.save_preset_button.get_child().set_label("")
        self.props.active_window.save_preset_button.get_child().set_tooltip_text(
            _("Save Changes")
        )

    def reload_variables(self):
        parsing_errors = []
        gtk_css = self.generate_gtk_css("gtk4")
        css_provider = Gtk.CssProvider()

        def on_error(_, section, error):
            start_location = section.get_start_location().chars
            end_location = section.get_end_location().chars
            line_number = section.get_end_location().lines
            parsing_errors.append(
                {
                    "error": error.message,
                    "element": gtk_css[start_location:end_location].strip(),
                    "line": gtk_css.splitlines()[line_number]
                    if line_number < len(gtk_css.splitlines())
                    else "<last line>",
                }
            )

        css_provider.connect("parsing-error", on_error)
        css_provider.load_from_data(gtk_css.encode())
        self.props.active_window.update_errors(
            self.global_errors + parsing_errors)
        # loading with the priority above user to override the applied config
        if self.current_css_provider is not None:
            Gtk.StyleContext.remove_provider_for_display(
                Gdk.Display.get_default(), self.current_css_provider
            )
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_USER + 1,
        )
        self.current_css_provider = css_provider

        self.is_ready = True

    def load_preset_action(self, _unused, *args):
        if args[0].get_string().startswith("custom-"):
            self.load_preset_from_file(
                os.path.join(
                    os.environ.get("XDG_CONFIG_HOME",
                                   os.environ["HOME"] + "/.config"),
                    "presets",
                    args[0].get_string().replace("custom-", "", 1) + ".json",
                )
            )
        else:
            self.load_preset_from_resource(
                f"{rootdir}/presets/" + args[0].get_string() + ".json"
            )
        Gio.SimpleAction.set_state(self.lookup_action("load_preset"), args[0])

    def show_apply_color_scheme_dialog(self, *_args):
        dialog = GradienceAppTypeDialog(
            _("Apply This Color Scheme?"),
            _(
                "Warning: any custom CSS files for those app types will be "
                "irreversibly overwritten!"
            ),
            "apply",
            _("Apply"),
            Adw.ResponseAppearance.SUGGESTED,
            transient_for=self.props.active_window,
        )

        dialog.connect("response", self.apply_color_scheme)
        dialog.present()

    def show_restore_color_scheme_dialog(self, *_args):
        dialog = GradienceAppTypeDialog(
            _("Restore applied color scheme?"),
            _("Make sure you have the current settings saved as a preset."),
            "restore",
            _("Restore"),
            Adw.ResponseAppearance.DESTRUCTIVE,
            transient_for=self.props.active_window,
        )
        dialog.connect("response", self.restore_color_scheme)
        dialog.present()

    def show_reset_color_scheme_dialog(self, *_args):
        dialog = GradienceAppTypeDialog(
            _("Reset applied color scheme?"),
            _("Make sure you have the current settings saved as a preset."),
            "reset",
            _("Reset"),
            Adw.ResponseAppearance.DESTRUCTIVE,
            transient_for=self.props.active_window,
        )
        dialog.connect("response", self.reset_color_scheme)
        dialog.present()

    def show_save_preset_dialog(self, *_args):
        dialog = Adw.MessageDialog(
            transient_for=self.props.active_window,
            heading=_("Save preset as…"),
            body=_(
                "Saving preset to <tt>{0}</tt>. If that preset already "
                "exists, it will be overwritten!"
            ).format(
                os.path.join(
                    os.environ.get("XDG_CONFIG_HOME",
                                   os.environ["HOME"] + "/.config"),
                    "presets",
                    "user",
                    to_slug_case(self.preset_name) + ".json",
                )
            ),
            body_use_markup=True,
        )

        dialog.add_response("cancel", _("Cancel"))
        dialog.add_response("save", _("Save"))
        dialog.set_response_appearance(
            "save", Adw.ResponseAppearance.SUGGESTED)
        dialog.set_default_response("cancel")
        dialog.set_close_response("cancel")

        preset_entry = Gtk.Entry(placeholder_text="Preset Name")
        preset_entry.set_text(self.preset_name)

        def on_preset_entry_change(*_args):
            if len(preset_entry.get_text()) == 0:
                dialog.set_body(
                    _(
                        "Saving preset to <tt>{0}</tt>. If that preset "
                        "already exists, it will be overwritten!"
                    ).format(
                        os.path.join(
                            os.environ.get(
                                "XDG_CONFIG_HOME", os.environ["HOME"] +
                                "/.config"
                            ),
                            "presets",
                            "user",
                        )
                    )
                )
                dialog.set_response_enabled("save", False)
            else:
                dialog.set_body(
                    _(
                        "Saving preset to <tt>{0}</tt>. If that preset "
                        "already exists, it will be overwritten!"
                    ).format(
                        os.path.join(
                            os.environ.get(
                                "XDG_CONFIG_HOME", os.environ["HOME"] +
                                "/.config"
                            ),
                            "presets",
                            "user",
                            to_slug_case(preset_entry.get_text()) + ".json",
                        )
                    )
                )
                dialog.set_response_enabled("save", True)

        preset_entry.connect("changed", on_preset_entry_change)
        dialog.set_extra_child(preset_entry)

        dialog.connect("response", self.save_preset, preset_entry)

        dialog.present()

    def show_exit_dialog(self, *_args):
        dialog = Adw.MessageDialog(
            transient_for=self.props.active_window,
            heading=_("You have unsaved changes!"),
            body=_(
                "Saving preset to <tt>{0}</tt>. If that preset already "
                "exists, it will be overwritten!"
            ).format(
                os.path.join(
                    os.environ.get("XDG_CONFIG_HOME",
                                   os.environ["HOME"] + "/.config"),
                    "presets",
                    "user",
                    to_slug_case(self.preset_name) + ".json",
                )
            ),
            body_use_markup=True,
        )

        dialog.add_response("cancel", _("Cancel"))
        dialog.add_response("discard", _("Discard"))
        dialog.add_response("save", _("Save"))
        dialog.set_response_appearance(
            "save", Adw.ResponseAppearance.SUGGESTED)
        dialog.set_response_appearance(
            "discard", Adw.ResponseAppearance.DESTRUCTIVE)
        dialog.set_default_response("cancel")
        dialog.set_close_response("cancel")

        preset_entry = Gtk.Entry(placeholder_text="Preset Name")
        preset_entry.set_text(self.preset_name)

        def on_preset_entry_change(*_args):
            if len(preset_entry.get_text()) == 0:
                dialog.set_body(
                    _(
                        "Saving preset to <tt>{0}</tt>. If that preset "
                        "already exists, it will be overwritten!"
                    ).format(
                        os.path.join(
                            os.environ.get(
                                "XDG_CONFIG_HOME", os.environ["HOME"] +
                                "/.config"
                            ),
                            "presets",
                            "user",
                        )
                    )
                )
                dialog.set_response_enabled("save", False)
            else:
                dialog.set_body(
                    _(
                        "Saving preset to <tt>{0}</tt>. If that preset "
                        "already exists, it will be overwritten!"
                    ).format(
                        os.path.join(
                            os.environ.get(
                                "XDG_CONFIG_HOME", os.environ["HOME"] +
                                "/.config"
                            ),
                            "presets",
                            "user",
                            to_slug_case(preset_entry.get_text()) + ".json",
                        )
                    )
                )
                dialog.set_response_enabled("save", True)

        preset_entry.connect("changed", on_preset_entry_change)
        dialog.set_extra_child(preset_entry)

        dialog.connect("response", self.save_preset, preset_entry)

        dialog.present()

    def save_preset(self, _unused, response, entry):
        if response == "save":
            self.preset.save_preset(entry.get_text(), self.plugins_list)
            self.clear_dirty()
            self.win.toast_overlay.add_toast(
                Adw.Toast(title=_("Preset saved")))
        elif response == "discard":
            self.clear_dirty()
            self.win.close()

    def apply_color_scheme(self, widget, response):
        if response == "apply":
            if widget.get_app_types()["gtk4"]:
                gtk4_dir = os.path.join(
                    os.environ.get("XDG_CONFIG_HOME",
                                   os.environ["HOME"] + "/.config"),
                    "gtk-4.0",
                )
                if not os.path.exists(gtk4_dir):
                    os.makedirs(gtk4_dir)
                gtk4_css = self.generate_gtk_css("gtk4")
                contents = ""
                try:
                    with open(
                        os.path.join(gtk4_dir, "gtk.css"), "r", encoding="utf-8"
                    ) as file:
                        contents = file.read()
                except FileNotFoundError:  # first run
                    pass
                else:
                    with open(
                        os.path.join(gtk4_dir, "gtk.css.bak"), "w", encoding="utf-8"
                    ) as file:
                        file.write(contents)
                finally:
                    with open(
                        os.path.join(gtk4_dir, "gtk.css"), "w", encoding="utf-8"
                    ) as file:
                        file.write(gtk4_css)

            if widget.get_app_types()["gtk3"]:
                gtk3_dir = os.path.join(
                    os.environ.get("XDG_CONFIG_HOME",
                                   os.environ["HOME"] + "/.config"),
                    "gtk-3.0",
                )
                if not os.path.exists(gtk3_dir):
                    os.makedirs(gtk3_dir)
                gtk3_css = self.generate_gtk_css("gtk3")
                contents = ""
                try:
                    with open(
                        os.path.join(gtk3_dir, "gtk.css"), "r", encoding="utf-8"
                    ) as file:
                        contents = file.read()
                except FileNotFoundError:  # first run
                    pass
                else:
                    with open(
                        os.path.join(gtk3_dir, "gtk.css.bak"), "w", encoding="utf-8"
                    ) as file:
                        file.write(contents)
                finally:
                    with open(
                        os.path.join(gtk3_dir, "gtk.css"), "w", encoding="utf-8"
                    ) as file:
                        file.write(gtk3_css)

            self.reload_plugins()
            self.plugins_list.apply()

            self.win.toast_overlay.add_toast(
                Adw.Toast(title=_("Preset set sucessfully"))
            )

            dialog = Adw.MessageDialog(
                transient_for=self.props.active_window,
                heading=_("Log out ?"),
                body=_(
                    "For the changes to take effect, you need to log out. "
                ),
                body_use_markup=True,
            )

            dialog.add_response("cancel", _("Cancel"))
            dialog.add_response("logout", _("Logout"))
            dialog.set_response_appearance(
                "logout", Adw.ResponseAppearance.DESTRUCTIVE)
            dialog.set_default_response("cancel")
            dialog.set_close_response("cancel")

            dialog.connect('response', self.on_logout_dialog_response)
            dialog.present()

    def on_logout_dialog_response (self, dialog, response):
        if response == "logout":
            print("logout")
            run_command(['gnome-session-quit', '--no-prompt'])

    def restore_color_scheme(self, widget, response):
        if response == "restore":
            if widget.get_app_types()["gtk4"]:
                file = Gio.File.new_for_path(
                    os.path.join(
                        os.environ.get(
                            "XDG_CONFIG_HOME", os.environ["HOME"] + "/.config"
                        ),
                        "gtk-4.0/gtk.css.bak",
                    )
                )
                try:
                    backup = open(
                        os.path.join(
                            os.environ.get(
                                "XDG_CONFIG_HOME", os.environ["HOME"] +
                                "/.config"
                            ),
                            "gtk-4.0/gtk.css.bak",
                        ),
                        "r",
                        encoding="utf-8",
                    )
                    contents = backup.read()
                    backup.close()
                    gtk4css = open(
                        os.path.join(
                            os.environ.get(
                                "XDG_CONFIG_HOME", os.environ["HOME"] +
                                "/.config"
                            ),
                            "gtk-4.0/gtk.css",
                        ),
                        "w",
                        encoding="utf-8",
                    )
                    gtk4css.write(contents)
                    gtk4css.close()
                except FileNotFoundError:
                    self.win.toast_overlay.add_toast(
                        Adw.Toast(title=_("Could not restore GTK 4 backup"))
                    )

    def reset_color_scheme(self, widget, response):
        if response == "reset":
            if widget.get_app_types()["gtk4"]:
                file = Gio.File.new_for_path(
                    os.path.join(
                        os.environ.get(
                            "XDG_CONFIG_HOME", os.environ["HOME"] + "/.config"
                        ),
                        "gtk-4.0/gtk.css",
                    )
                )
                try:
                    file.delete()
                except Exception:
                    pass

            if widget.get_app_types()["gtk3"]:
                file = Gio.File.new_for_path(
                    os.path.join(
                        os.environ.get(
                            "XDG_CONFIG_HOME", os.environ["HOME"] + "/.config"
                        ),
                        "gtk-3.0/gtk.css",
                    )
                )
                try:
                    file.delete()
                except Exception:
                    pass
            self.win.toast_overlay.add_toast(
                Adw.Toast(title=_("Preset reseted")))

    def show_preferences(self, *_args):
        prefs = GradiencePreferencesWindow(self.win)
        prefs.set_transient_for(self.win)
        prefs.present()

    def show_about_window(self, *_args):
        about = Adw.AboutWindow(
            transient_for=self.props.active_window,
            application_name=_("Gradience"),
            application_icon=app_id,
            developer_name=_("Gradience Team"),
            website=project_url,
            support_url=help_url,
            issue_url=bugtracker_url,
            developers=[
                "0xMRTT https://github.com/0xMRTT",
                "Artyom Fomin https://github.com/ArtyIF",
                "Verantor https://github.com/Verantor",
                "tfuxu https://github.com/tfuxu",
                "u1F98E https://github.com/u1f98e",
            ],
            artists=["David Lapshin https://github.com/daudix-UFO"],
            designers=["David Lapshin https://github.com/daudix-UFO"],
            documenters=[
                "0xMRTT https://github.com/0xMRTT",
                "David Lapshin https://github.com/daudix-UFO"
            ],
            # Translators: This is a place to put your credits (formats:
            # "Name https://example.com" or "Name <email@example.com>",
            # no quotes) and is not meant to be translated literally.
            translator_credits="""0xMRTT https://github.com/0xMRTT
                                    엘련 (Jisu Kim) https://github.com/vbalien
                Aggelos Tselios https://www.transifex.com/user/profile/AndroGR
                BritishBenji https://github.com/BritishBenji
                David Lapshin https://github.com/daudix-UFO
                Davide Ferracin https://github.com/phaerrax
                Ewout van Mansom https://github.com/emansom
                FineFindus https://github.com/FineFindus
                Gabriel Lemos https://github.com/gbrlgn
                Juanjo Cillero https://www.transifex.com/user/profile/renux918
                JungHee Lee https://github.com/MarongHappy
                K.B.Dharun Krishna https://github.com/kbdharun
                Karol Lademan https://www.transifex.com/user/profile/karlod
                Luna Jernberg https://github.com/bittin
                Maxime V https://www.transifex.com/user/profile/Adaoh
                Michal S. <michal@getcryst.al>
                Monty Monteusz https://www.transifex.com/user/profile/MontyQIQI
                Philip Goto https://github.com/flipflop97
                Renato Corrêa https://github.com/renatocrrs
                Rene Coty https://github.com/rene-coty
                Sabri Ünal https://github.com/libreajans
                Taylan Tatlı https://www.transifex.com/user/profile/TaylanTatli34
                bzizmza https://github.com/bzizmza
                muzena https://github.com/muzena
                renatocrrs https://github.com/renatocrrs
                tfuxu https://github.com/tfuxu
                yangyangdaji https://github.com/yangyangdaji
                Óscar Fernández Díaz https://github.com/oscfdezdz""",
            copyright="© 2022 Gradience Team",
            license_type=Gtk.License.GPL_3_0,
            version=version,
            release_notes_version=rel_ver,
            release_notes=_(
"""
<ul>
<li>Added ability to star preset to display it in Palette</li>
<li>Updated Firefox GNOME Theme plugin</li>
<li>Welcome screen have been improved</li>
<li>Margins in color info popovers are fixed</li>
<li>Added filter to search presets by repo</li>
<li>Added "No Preferences" window</li>
<li>Preset Manager window size have changed</li>
<li>"Offline" and "Nothing Found" pages have been added to Preset Manager</li>
<li>All text have been rewritten to follow GNOME Writing Guides</li>
<li>Switch from aiohttp to Libsoup3</li>
<li>Migrate to GNOME SDK 43</li>
<li>All contributors have been added to "About" window</li>
<li>Added "Log Out" dialog after preset apply</li>
<li>Some symbolics have changed, removed unnecessary hardcoded symbolics</li>
<li>Flatpak theme override now fixed</li>
<li>New and updated translations</li>
</ul>
"""
            ),
            comments=_(
"""
Gradience is a tool for customizing Libadwaita applications and the adw-gtk3 \
theme.
With Gradience you can:

- Change any color of Adwaita theme
- Apply Material 3 colors from wallpaper
- Use other users presets
- Change advanced options with CSS
- Extend functionality using plugins

This app is written in Python and uses GTK 4 and Libadwaita.
"""
            ),
        )
        about.add_credit_section(
            _("Plugins by"),
            [
                "0xMRTT https://github.com/0xMRTT",
                "Apisu https://github.com/aspizu",
            ],
        )
        about.add_credit_section(
            _("Presets by"),
            [
                "0xMRTT https://github.com/0xMRTT",
                "Ben Mitchell https://github.com/crispyricepc",
                "David Lapshin https://github.com/daudix-UFO",
                "JoshM-Yoru https://github.com/JoshM-Yoru",
                "José Hunter https://github.com/halfmexican",
                "Kainoa Kanter https://github.com/ThatOneCalculator",
                "Link Dupont https://github.com/subpop",
                "Luis David López https://github.com/lopeztel",
                "Mohammad Saleh Kamyab https://github.com/mskf1383",
                "Sal Watson https://github.com/salarua",
                "TeryVeneno https://github.com/TeryVeneno",
                "arslee https://github.com/arslee07",
                "badlydrawnface https://github.com/badlydrawnface",
                "cmagnificent https://github.com/cmagnificent",
                "hericiumvevo https://github.com/hericiumvevo",
                "tfuxu https://github.com/tfuxu",
                "zehkira https://github.com/zehkira",
            ],
        )
        about.add_credit_section(
            _("Packages by"),
            [
                "0xMRTT https://github.com/0xMRTT",
                "Lyes Saadi https://github.com/lyessaadi",
            ],
        )
        about.add_credit_section(
            _("Fixes by"),
            [
                "Erick Howard https://github.com/DivineBicycle",
                "Hari Rana https://github.com/TheEvilSkeleton",
                "José Hunter https://github.com/halfmexican",
                "Sabri Ünal https://github.com/libreajans",
                "Sal Watson https://github.com/salarua",
            ],
        )
        about.add_acknowledgement_section(
            _("Special thanks to"),
            [
                "Artyom Fomin https://github.com/ArtyIF",
                "Weblate https://weblate.org",
            ],
        )

        about.present()

    def update_custom_css_text(self, app_type, new_value):
        self.custom_css[app_type] = new_value
        self.reload_variables()

    def create_action(self, name, callback, shortcuts=None):
        """Add an application action.

        Args:
            name: the name of the action
            callback: the function to be called when the action is
              activated
            shortcuts: an optional list of accelerators
        """
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)

    def create_stateful_action(
        self, name, parameter_type, initial_state, callback, shortcuts=None
    ):
        """Add a stateful application action."""
        action = Gio.SimpleAction.new_stateful(
            name, parameter_type, initial_state)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)

    def setup_plugins(self):
        buglog("setup plugins")
        self.plugins_group = self.plugins_list.to_group()

        self.win.content_plugins.add(self.plugins_group)
        self.plugins_group = self.plugins_group

        self.custom_css_group = GradienceCustomCSSGroup()
        for app_type in settings_schema["custom_css_app_types"]:
            self.custom_css[app_type] = ""
        self.custom_css_group.load_custom_css(self.custom_css)
        self.win.content_plugins.add(self.custom_css_group)
        self.custom_css_group = self.custom_css_group

        plugins_errors = self.plugins_list.validate()

        self.props.active_window.update_errors(
            self.global_errors + plugins_errors)

    def reload_plugins(self):
        self.plugins_list.reload()
        buglog("reload plugins")
        self.win.content_plugins.remove(self.plugins_group)
        self.win.content_plugins.remove(self.custom_css_group)

        self.plugins_group = self.plugins_list.to_group()

        self.win.content_plugins.add(self.plugins_group)
        self.plugins_group = self.plugins_group

        self.custom_css_group = GradienceCustomCSSGroup()
        for app_type in settings_schema["custom_css_app_types"]:
            self.custom_css[app_type] = ""
        self.custom_css_group.load_custom_css(self.custom_css)
        self.win.content_plugins.add(self.custom_css_group)
        self.custom_css_group = self.custom_css_group

        plugins_errors = self.plugins_list.validate()

        self.props.active_window.update_errors(
            self.global_errors + plugins_errors)

    @staticmethod
    def show_adwaita_demo(*_args):
        GLib.spawn_command_line_async(
            'sh -c "/bin/adwaita-1-demo > /dev/null 2>&1"')

    @staticmethod
    def show_gtk4_demo(*_args):
        GLib.spawn_command_line_async(
            'sh -c "/bin/gtk4-demo > /dev/null 2>&1"')

    @staticmethod
    def show_gtk4_widget_factory(*_args):
        GLib.spawn_command_line_async(
            'sh -c "/bin/gtk4-widget-factory > /dev/null 2>&1"'
        )


def main():
    """The application's entry point."""
    app = GradienceApplication()
    return app.run(sys.argv)
