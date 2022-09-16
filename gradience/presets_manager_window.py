# presets_manager_window.py
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
from random import random
import shutil
import json

from pathlib import Path

from gi.repository import Gtk, Adw, GLib

from .preset_row import GradiencePresetRow
from .builtin_preset_row import GradienceBuiltinPresetRow
from .explore_preset_row import GradienceExplorePresetRow
from .modules.custom_presets import fetch_presets
from .repo_row import GradienceRepoRow
from .modules.utils import buglog
from .constants import rootdir

import random

from constants import BADGE_COLORS

@Gtk.Template(resource_path=f"{rootdir}/ui/presets_manager_window.ui")
class GradiencePresetWindow(Adw.Window):
    __gtype_name__ = "GradiencePresetWindow"

    installed = Gtk.Template.Child()
    repos = Gtk.Template.Child()
    main_view = Gtk.Template.Child()
    toast_overlay = Gtk.Template.Child()

    import_button = Gtk.Template.Child()
    import_file_chooser = Gtk.Template.Child()

    all_filter = Gtk.Template.Child()
    json_filter = Gtk.Template.Child()

    remove_button = Gtk.Template.Child("remove_button")
    file_manager_button = Gtk.Template.Child("file_manager_button")

    search_entry = Gtk.Template.Child("search_entry")
    search_stack = Gtk.Template.Child("search_stack")
    search_results = Gtk.Template.Child("search_results")
    search_spinner = Gtk.Template.Child("search_spinner")
    search_dropdown = Gtk.Template.Child("search_dropdown")
    search_string_list = Gtk.Template.Child("search_string_list")

    custom_presets = {}

    official_repositories = {
        _(
            "Official"
        ): "https://github.com/GradienceTeam/Community/raw/next/official.json",
    }

    search_results_list = []

    def __init__(self, parent, **kwargs):
        super().__init__(**kwargs)

        self.app = Gtk.Application.get_default()

        self.parent = parent

        self.settings = parent.settings

        self.user_repositories = self.settings.get_value("repos").unpack()
        self.user_repositories[
            _("Curated")
        ] = "https://github.com/GradienceTeam/Community/raw/next/curated.json"
        self.enabled_repos = self.settings.get_value("enabled-repos").unpack()

        self.setup_signals()
        self.setup()

        self.setup_builtin_presets()
        self.setup_repos()
        self.setup_user_presets()
        self.setup_explore()

    def setup(self):
        self.import_file_chooser.set_transient_for(self)
        self.import_file_chooser.set_action(Gtk.FileChooserAction.OPEN)

        self.import_file_chooser.add_filter(self.all_filter)
        self.import_file_chooser.add_filter(self.json_filter)

        self.import_file_chooser.connect(
            "response", self.on_file_chooser_response)

    def setup_signals(self):
        self.search_entry.connect("search-changed", self.on_search_changed)
        self.search_entry.connect("stop-search", self.on_search_ended)

    def setup_builtin_presets(self):
        self.builtin_preset_list = Adw.PreferencesGroup()
        self.builtin_preset_list.set_title(_("Builtin Presets"))
        self.installed.add(self.builtin_preset_list)

    def setup_user_presets(self):
        self.preset_list = Adw.PreferencesGroup()
        self.preset_list.set_title(_("User Presets"))
        self.installed.add(self.preset_list)
        self.reload_pref_group()

    def setup_repos(self):
        self.repos_list = Adw.PreferencesGroup()
        self.repos_list.set_title(_("Repositories"))
        self.repos.add(self.repos_list)
        self.reload_repos_group()

    def setup_explore(self):
        self.search_results_list.clear()
        buglog("Preset list cleared")

        offline = False

        def fetch(repo_name, repo, badge):
            global offline
            explore_presets, urls = fetch_presets(repo)

            if explore_presets:
                self.search_spinner.props.visible = False

                for (preset, preset_name), preset_url in zip(
                    explore_presets.items(), urls
                ):
                    row = GradienceExplorePresetRow(
                        preset_name, preset_url, self, repo_name, badge
                    )
                    self.search_results.append(row)
                    self.search_results_list.append(row)
            else:
                offline = True

        print(self._repos)
        for repo_name, repo in self._repos.items():
            self.search_string_list.append(repo_name)
            badge_color = random.choice(BADGE_COLORS)
            buglog(
                f"Selected badge color: {badge_color} if it's look bad, please report it"
            )
            fetch(repo_name=repo_name, repo=repo, badge=badge_color)

        if offline:
            self.search_spinner.props.visible = False
            self.search_stack.set_visible_child_name("page_offline")

    def add_repo(self, _unused, response, name_entry, url_entry):
        if response == "add":
            repo = {name_entry.get_text(): url_entry.get_text()}
            self.user_repositories.update(repo)

            self.save_repos()

    def remove_repo(self, repo_name):
        self.user_repositories.pop(repo_name)
        self.save_repos()

    def save_repos(self):
        self.settings.set_value("repos", GLib.Variant(
            "a{sv}", self.user_repositories))
        self.reload_repos_group()
        self.setup_explore()

    def on_add_repo_button_clicked(self, *args):
        dialog = Adw.MessageDialog(
            transient_for=self,
            heading=_("Add new repository"),
            body=_("Add a repository to install additional presets"),
            body_use_markup=True,
        )

        # TODO: Fix "assertion 'adw_message_dialog_has_response (self, response)' failed" error \
        # (don't know if this isn't a bug in libadwaita itself)
        dialog.add_response("cancel", _("Cancel"))
        dialog.add_response("add", _("Add"))
        dialog.set_response_appearance("add", Adw.ResponseAppearance.SUGGESTED)
        dialog.set_default_response("cancel")
        dialog.set_close_response("cancel")

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)

        name_entry = Gtk.Entry(placeholder_text="Preset Name")
        name_entry.set_text("My Repo")

        def on_name_entry_change(*_args):
            if len(name_entry.get_text()) == 0:
                dialog.set_response_enabled("save", False)
            else:
                dialog.set_response_enabled("save", True)

        name_entry.connect("changed", on_name_entry_change)

        url_entry = Gtk.Entry(
            placeholder_text="https://website.com/raw/presets.json")

        def on_url_entry_change(*_args):
            if len(url_entry.get_text()) == 0:
                dialog.set_response_enabled("save", False)
            else:
                # TODO: Check if URL is valid
                dialog.set_response_enabled("save", True)

        url_entry.connect("changed", on_url_entry_change)

        box.append(name_entry)
        box.append(url_entry)
        dialog.set_extra_child(box)

        dialog.connect("response", self.add_repo, name_entry, url_entry)

        dialog.present()

    def on_search_changed(self, *args):
        search_text = self.search_entry.props.text
        buglog("[New search query]")
        buglog(f"Presets amount: {len(self.search_results_list)}")
        buglog(f"Search string: {search_text}")
        buglog("Items found:")
        for widget in self.search_results_list:
            if search_text == "":
                widget.props.visible = True
            else:
                widget.props.visible = False
                if (
                    not self.search_dropdown.props.selected_item.get_string().lower()
                    in "all"
                ):
                    if (
                        self.search_dropdown.props.selected_item.get_string().lower()
                        in widget.prefix.lower()
                    ):
                        if search_text.lower() in widget.props.title.lower():
                            widget.props.visible = True
                            buglog(widget.props.title)
                else:
                    if search_text.lower() in widget.props.title.lower():
                        widget.props.visible = True
                        buglog(widget.props.title)

    def on_search_ended(self, *args):
        for widget in self.search_results_list:
            widget.props.visible = True

    @Gtk.Template.Callback()
    def on_file_manager_button_clicked(self, *_args):
        self.app.open_preset_directory()

    @Gtk.Template.Callback()
    def on_import_button_clicked(self, *_args):
        self.import_file_chooser.show()

    def on_file_chooser_response(self, widget, response):
        if response == Gtk.ResponseType.ACCEPT:
            self.preset_path = widget.get_file()
            preset_file = self.preset_path.get_basename()
        widget.hide()

        if response == Gtk.ResponseType.ACCEPT:
            if preset_file.endswith(".json"):

                if preset_file.strip(".json") in self.custom_presets:
                    self.toast_overlay.add_toast(
                        Adw.Toast(title=_("Preset already exists"))
                    )
                else:
                    shutil.copy(
                        self.preset_path.get_path(),
                        os.path.join(
                            os.environ.get(
                                "XDG_CONFIG_HOME", os.environ["HOME"] +
                                "/.config"
                            ),
                            "presets",
                            preset_file,
                        ),
                    )
                    self.toast_overlay.add_toast(
                        Adw.Toast(title=_("Preset imported")))
            else:
                self.toast_overlay.add_toast(
                    Adw.Toast(title=_("Unsupported file format, must be .json"))
                )

        self.reload_pref_group()

    def reload_pref_group(self):
        print("reload")
        preset_directory = os.path.join(
            os.environ.get("XDG_CONFIG_HOME", os.environ["HOME"] + "/.config"),
            "presets",
        )
        if not os.path.exists(preset_directory):
            os.makedirs(preset_directory)

        self.custom_presets = {"user": {}}
        self.builtin_presets = {
            "adwaita-dark": "Adwaita Dark",
            "adwaita": "Adwaita",
            "pretty-purple": "Pretty Purple",
        }
        for repo in Path(preset_directory).iterdir():
            if repo.is_dir():  # repo
                presets_list = {}
                for file_name in repo.iterdir():
                    file_name = str(file_name)
                    if file_name.endswith(".json"):
                        try:
                            with open(
                                os.path.join(preset_directory, file_name),
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
                            self.toast_overlay.add_toast(
                                Adw.Toast(title=_("Failed to load preset"))
                            )
                self.custom_presets[repo.name] = presets_list
            elif repo.is_file():
                buglog("file")
                # keep compatiblity with old presets
                if repo.name.endswith(".json"):
                    os.rename(repo, os.path.join(
                        preset_directory, "user", repo.name))

                    try:
                        with open(
                            os.path.join(preset_directory, "user", repo),
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
                        self.toast_overlay.add_toast(
                            Adw.Toast(title=_("Failed to load preset"))
                        )
                    buglog(self.custom_presets)
        self.installed.remove(self.preset_list)
        self.installed.remove(self.builtin_preset_list)

        print("reload 2")

        self.builtin_preset_list = Adw.PreferencesGroup()
        self.builtin_preset_list.set_title(_("Builtin Presets"))
        for preset, preset_name in self.builtin_presets.items():
            row = GradienceBuiltinPresetRow(preset_name, self.toast_overlay)
            self.builtin_preset_list.add(row)
        self.installed.add(self.builtin_preset_list)

        self.preset_list = Adw.PreferencesGroup()
        self.preset_list.set_title(_("User Presets"))
        self.preset_list.set_description(
            _(
                'See <a href="https://github.com/GradienceTeam/Community">GradienceTeam/Community</a> on Github for more presets'
            )
        )

        buglog(f"custom_presets values: {self.custom_presets.values()}")

        presets_check = not (
            len(self.custom_presets["user"]) == 0
            and len(self.custom_presets["official"]) == 0
            and len(self.custom_presets["curated"]) == 0
        )
        buglog(f"preset_check: {presets_check}")

        print("reload 3")

        if presets_check:
            for repo, presets in self.custom_presets.items():
                for preset, preset_name in presets.items():
                    row = GradiencePresetRow(preset_name, self, repo)
                    self.preset_list.add(row)

        else:
            self.preset_empty = Adw.ActionRow()
            self.preset_empty.set_title(
                _(
                    "No preset found! Use the import button to import one or search one on the Explore tab"
                )
            )
            self.preset_list.add(self.preset_empty)
        self.installed.add(self.preset_list)
        print("reload end")

    def reload_repos_group(self):
        self.repos.remove(self.repos_list)
        self.repos_list = Adw.PreferencesGroup()
        self.repos_list.set_title(_("Repositories"))

        self.add_repo_button = Gtk.Button.new_from_icon_name(
            "list-add-symbolic")
        self.add_repo_button.connect(
            "clicked", self.on_add_repo_button_clicked)

        self.repos_list.set_header_suffix(self.add_repo_button)

        for repo_name, repo in self.official_repositories.items():
            row = GradienceRepoRow(repo, repo_name, self, deletable=False)
            self.repos_list.add(row)

        for repo_name, repo in self.user_repositories.items():
            row = GradienceRepoRow(repo, repo_name, self)
            self.repos_list.add(row)

        self.repos.add(self.repos_list)

        self._repos = {**self.user_repositories, **self.official_repositories}
