# preset_row.py
#
# Change the look of Adwaita, with ease
# Copyright (C) 2022  Gradience Team
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

import os

from gi.repository import Gtk, Adw, Xdp, XdpGtk4

from gradience.frontend.views.share_window import GradienceShareWindow
from gradience.backend.utils.common import to_slug_case
from gradience.backend.models.preset import Preset
from gradience.backend.constants import rootdir

from gradience.backend.logger import Logger

logging = Logger()


@Gtk.Template(resource_path=f"{rootdir}/ui/preset_row.ui")
class GradiencePresetRow(Adw.ExpanderRow):
    __gtype_name__ = "GradiencePresetRow"

    name_entry = Gtk.Template.Child("name_entry")
    value_stack = Gtk.Template.Child("value_stack")
    name_entry_toggle = Gtk.Template.Child("name_entry_toggle")
    apply_button = Gtk.Template.Child("apply_button")
    remove_button = Gtk.Template.Child("remove_button")
    btn_report = Gtk.Template.Child("btn_report")
    # btn_share = Gtk.Template.Child("btn_share")
    star_button = Gtk.Template.Child("star_button")
    badge_list = Gtk.Template.Child("badge_list")
    no_badges = Gtk.Template.Child("no_badges")

    def __init__(self, name, preset_path, win, repo_name, author="", **kwargs):
        super().__init__(**kwargs)

        self.name = name

        self.prefix = to_slug_case(repo_name)

        self.set_name(name)
        self.set_title(name)
        self.set_subtitle(repo_name)
        self.name_entry.set_text(name)

        self.app = Gtk.Application.get_default()
        self.win = win
        self.toast_overlay = self.win.toast_overlay

        self.preset = Preset().new_from_path(preset_path)

        if self.preset.badges:
            self.has_badges = True
            self.no_badges.set_visible(False)

            for badge_name in self.preset.badges:
                badge = Gtk.Label(label=badge_name.capitalize())
                badge.get_style_context().add_class("tag")
                badge.set_valign(Gtk.Align.CENTER)
                badge.get_style_context().add_class("caption")
                badge.get_style_context().add_class(f"badge-{badge}")
                self.badge_list.append(badge)
        else:
            self.has_badges = False
            self.no_badges.set_visible(True)

        self.btn_report.connect("clicked", self.on_report_btn_clicked)
        # self.btn_share.connect("clicked", self.on_share_btn_clicked)
        self.star_button.connect("clicked", self.on_star_button_clicked)

        if name in self.win.app.favourite:
            self.star_button.set_icon_name("starred-symbolic")
            self.star_button.set_tooltip_text(_("Remove from Favorites"))
        else:
            self.star_button.set_icon_name("non-starred-symbolic")
            self.star_button.set_tooltip_text(_("Add to Favorites"))

    # def on_share_btn_clicked(self, *_args):
    #     win = GradienceShareWindow(self.win)
    #     win.present()

    def on_star_button_clicked(self, *_args):
        if self.name in self.win.app.favourite:
            self.win.app.favourite.remove(self.name)
            self.star_button.set_icon_name("non-starred-symbolic")
            self.star_button.set_tooltip_text(_("Add to Favorites"))
        else:
            self.win.app.favourite.add(self.name)
            self.star_button.set_icon_name("starred-symbolic")
            self.star_button.set_tooltip_text(_("Remove from Favorites"))
        self.win.app.save_favourite()
        self.win.reload_pref_group()

    @Gtk.Template.Callback()
    def on_apply_button_clicked(self, *_args):
        self.app.load_preset_from_file(self.preset.preset_path)

    def on_undo_button_clicked(self, *_args):
        self.delete_preset = False
        self.delete_toast.dismiss()

    @Gtk.Template.Callback()
    def on_name_entry_changed(self, *_args):
        self.name = self.name_entry.get_text()
        self.set_name(self.name)
        self.set_title(self.name)

    @Gtk.Template.Callback()
    def on_name_entry_toggled(self, *_args):
        if self.name_entry_toggle.get_active():
            self.value_stack.set_visible_child(self.name_entry)
        else:
            self.preset.rename(self.name_entry.get_text())
            self.value_stack.set_visible_child(self.apply_button)

    def on_report_btn_clicked(self, *_args):
        parent = XdpGtk4.parent_new_gtk(self.win)

        def open_dir_callback(_, result):
            self.app.portal.open_uri_finish(result)

        self.app.portal.open_uri(
            parent,
            "https://github.com/GradienceTeam/Community/issues/new?assignees=daudix-UFO&labels=bug&template=preset_issue.yml&title=preset%3A+",
            Xdp.OpenUriFlags.NONE,
            None,
            open_dir_callback,
        )

    @Gtk.Template.Callback()
    def on_remove_button_clicked(self, *_args):
        self.delete_preset = True
        self.delete_toast = Adw.Toast(title=_("Preset removed"))
        self.delete_toast.set_button_label(_("Undo"))
        self.delete_toast.connect("dismissed", self.on_delete_toast_dismissed)
        self.delete_toast.connect(
            "button-clicked", self.on_undo_button_clicked)

        self.toast_overlay.add_toast(self.delete_toast)

        try:
            os.rename(
                self.preset.preset_path,
                self.preset.preset_path + ".to_delete",
            )

            self.set_name(self.name + "(" + _("Pending Deletion") + ")")
        except Exception as e:
            logging.error(f"Unable to rename an preset for later deletion. Exc: {e}")
        else:
            self.props.visible = False
        finally:
            self.delete_preset = True

    def on_delete_toast_dismissed(self, widget):
        if self.delete_preset:
            logging.debug(f"Deleting preset {self.preset.display_name}")
            try:
                logging.debug("Preset filename:" + self.preset.preset_path + ".to_delete")
                os.remove(self.preset.preset_path + ".to_delete")
            except Exception as e:
                logging.error(f"Unable to delete an preset. Exc: {e}")
                self.toast_overlay.add_toast(
                    Adw.Toast(title=_("Unable to delete preset"))
                )
            finally:
                self.win.reload_pref_group()
        else:
            try:
                os.rename(
                    self.preset.preset_path + ".to_delete",
                    self.preset.preset_path
                )
            except Exception as e:
                logging.error(f"Unable to rename an preset. Exc: {e}")
            finally:
                self.win.reload_pref_group()

        self.delete_preset = True
