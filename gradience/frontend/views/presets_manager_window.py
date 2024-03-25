# presets_manager_window.py
#
# Change the look of Adwaita, with ease
# Copyright (C) 2022-2023, Gradience Team
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.``
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

import os
import shutil
import json

from pathlib import Path
from gi.repository import Gtk, Adw, GLib

from gradience.backend.utils.networking import get_preset_repos

from gradience.backend.preset_downloader import PresetDownloader
from gradience.backend.theming.preset import PresetUtils
from gradience.backend.globals import presets_dir
from gradience.backend.constants import rootdir

from gradience.frontend.widgets.preset_row import GradiencePresetRow
from gradience.frontend.widgets.builtin_preset_row import GradienceBuiltinPresetRow
from gradience.frontend.widgets.explore_preset_row import GradienceExplorePresetRow
from gradience.frontend.widgets.repo_row import GradienceRepoRow

from gradience.backend.logger import Logger

logging = Logger()


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
    report_button = Gtk.Template.Child("report_button")
    file_manager_button = Gtk.Template.Child("file_manager_button")

    search_entry = Gtk.Template.Child("search_entry")
    search_stack = Gtk.Template.Child("search_stack")
    search_results = Gtk.Template.Child("search_results")
    search_spinner = Gtk.Template.Child("search_spinner")
    search_dropdown = Gtk.Template.Child("search_dropdown")
    search_string_list = Gtk.Template.Child("search_string_list")

    custom_presets = {}

    search_results_list = []

    offline = False

    def __init__(self, parent, **kwargs):
        super().__init__(**kwargs)

        self.parent = parent
        self.settings = parent.settings
        self.app = self.parent.get_application()

        self.set_transient_for(self.app.get_active_window())

        self.user_repositories = self.settings.get_value("repos").unpack()
        self.enabled_repos = self.settings.get_value("enabled-repos").unpack()

        self.preset_repos = get_preset_repos(self.settings.get_boolean("use-jsdelivr"))

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
        self.search_dropdown.connect("notify", self.on_search_changed)
        self.search_entry.connect("stop-search", self.on_search_ended)

    def setup_builtin_presets(self):
        self.builtin_preset_list = Adw.PreferencesGroup()
        self.builtin_preset_list.set_title(_("Built-In Presets"))
        self.installed.add(self.builtin_preset_list)

    def setup_user_presets(self):
        self.preset_list = Adw.PreferencesGroup()
        self.preset_list.set_title(_("User Presets"))
        self.installed.add(self.preset_list)
        self.reload_pref_group()

    # TODO: Separate repositories list initialization from this function and remove Repositories tab in 1.0 release
    def setup_repos(self):
        self.repos_list = Adw.PreferencesGroup()
        self.repos_list.set_title(_("Repositories"))
        self.repos.add(self.repos_list)
        self.reload_repos_group()

    def setup_explore(self):
        self.search_results_list.clear()

        if self.offline:
            self.search_spinner.props.visible = False
            self.search_stack.set_visible_child_name("page_offline")

    def add_explore_rows(self):
        logging.debug(self._repos)

        for repo_name, repo in self._repos.items():
            self.search_string_list.append(repo_name)

            if repo_name == "Official":
                badge = "black"
            elif repo_name == "Curated":
                badge = "white"
            else:
                badge = "white"

            try:
                explore_presets, urls = PresetDownloader(self.settings.get_boolean("use-jsdelivr")).fetch_presets(repo)
            except GLib.GError as e:
                if e.code == 1:
                    self.offline = True
                    self.search_spinner.props.visible = False
                    self.search_stack.set_visible_child_name("page_offline")
                else:
                    self.search_spinner.props.visible = False
            # TODO: Create a new page to show for other errors eg. "page_error"
            except json.JSONDecodeError:
                self.search_spinner.props.visible = False
            else:
                self.search_spinner.props.visible = False

                for (preset, preset_name), preset_url in zip(
                    explore_presets.items(), urls
                ):
                    row = GradienceExplorePresetRow(
                        preset_name, preset_url, self, repo_name, badge
                    )
                    self.search_results.append(row)
                    self.search_results_list.append(row)

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
            body=_("Add a repository to install additional presets."),
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
        name_entry.set_text("Custom Repo")

        def on_name_entry_change(*_args):
            if len(name_entry.get_text()) == 0:
                dialog.set_response_enabled("save", False)
            else:
                dialog.set_response_enabled("save", True)

        name_entry.connect("changed", on_name_entry_change)

        url_entry = Gtk.Entry(
            placeholder_text="https://example.com/raw/presets.json")

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
        items_count = 0
        search_text = self.search_entry.props.text

        logging.debug("[New search query]")
        logging.debug(f"Preset amount: {len(self.search_results_list)}")
        logging.debug(f"Search string: {search_text}")
        logging.debug("Items found:")

        if not self.offline:
            self.search_stack.set_visible_child_name("page_results")
            for widget in self.search_results_list:
                widget.props.visible = False

                selected_item_pos = self.search_dropdown.get_selected()
                selected_item_name = self.search_dropdown.props.selected_item.get_string().lower()

                if not selected_item_pos == 0:
                    if selected_item_name in widget.prefix.lower():
                        if search_text.lower() in widget.props.title.lower():
                            widget.props.visible = True
                            items_count += 1
                            logging.debug(widget.props.title)
                else:
                    if search_text.lower() in widget.props.title.lower():
                        widget.props.visible = True
                        items_count += 1
                        logging.debug(widget.props.title)
                    elif search_text == "":
                        widget.props.visible = True
                        items_count += 1

            if items_count == 0:
                self.search_stack.set_visible_child_name("page_empty")

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

                if preset_file in self.custom_presets:
                    self.toast_overlay.add_toast(
                        Adw.Toast(title=_("Preset already exists"))
                    )
                else:
                    shutil.copy(
                        self.preset_path.get_path(),
                        os.path.join(
                            presets_dir,
                            "user",
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
        logging.debug("reload")

        if not os.path.exists(presets_dir):
            os.makedirs(presets_dir)

        self.custom_presets = {"user": {}}
        self.builtin_presets = {
            "adwaita": "Adwaita",
            "adwaita-dark": "Adwaita Dark",
            "pretty-purple": "Pretty Purple"
        }

        for repo in Path(presets_dir).iterdir():
            logging.debug(f"presets_dir.iterdir: {repo}")

            try:
                presets_list = PresetUtils().get_presets_list(repo)
            except (OSError, KeyError, AttributeError):
                logging.error("Failed to retrieve a list of presets.")
                self.toast_overlay.add_toast(
                    Adw.Toast(title=_("Failed to load list of presets"))
                )
            else:
                self.custom_presets[repo.name] = presets_list

        self.installed.remove(self.preset_list)
        self.installed.remove(self.builtin_preset_list)

        self.builtin_preset_list = Adw.PreferencesGroup()
        self.builtin_preset_list.set_title(_("Built-in Presets"))
        for preset, preset_name in self.builtin_presets.items():
            row = GradienceBuiltinPresetRow(preset_name, self.toast_overlay)
            self.builtin_preset_list.add(row)
        self.installed.add(self.builtin_preset_list)

        self.preset_list = Adw.PreferencesGroup()
        self.preset_list.set_title(_("User Presets"))
        self.preset_list.set_description(
            _(
                "See "
                '<a href="https://github.com/GradienceTeam/Community">'
                "GradienceTeam/Community</a> on Github for more presets."
            )
        )

        logging.debug(f"custom_presets: {self.custom_presets}")

        presets_check = not (
            len(self.custom_presets["user"]) == 0
            and len(self.custom_presets["official"]) == 0
            and len(self.custom_presets["curated"]) == 0
        )
        logging.debug(f"preset_check: {presets_check}")

        if presets_check:
            for repo, presets in self.custom_presets.items():
                for preset_file, preset_name in presets.items():
                    row = GradiencePresetRow(
                        preset_name, preset_file, self, repo)
                    self.preset_list.add(row)

        else:
            self.preset_empty = Adw.ActionRow()
            self.preset_empty.set_title(
                _(
                    "No preset found! Use the import button to import one or "
                    "search one on the Explore tab."
                )
            )
            self.preset_list.add(self.preset_empty)
        self.installed.add(self.preset_list)

    def reload_repos_group(self):
        self.repos.remove(self.repos_list)
        self.repos_list = Adw.PreferencesGroup()
        self.repos_list.set_title(_("Repositories"))

        for repo_name, repo in self.preset_repos.items():
            row = GradienceRepoRow(repo, repo_name, self, deletable=False)
            self.repos_list.add(row)

        for repo_name, repo in self.user_repositories.items():
            row = GradienceRepoRow(repo, repo_name, self)
            self.repos_list.add(row)

        self.repos.add(self.repos_list)

        self._repos = {**self.user_repositories, **self.preset_repos}

