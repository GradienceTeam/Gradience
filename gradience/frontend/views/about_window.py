# about_window.py
#
# Change the look of Adwaita, with ease
# Copyright (C) 2023, Gradience Team
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

from gi.repository import Gtk, Adw

from gradience.backend import constants


release_notes = """
<ul>
<li>Only configure local CLI if buildtype is set to debug</li>
<li>Changed margins in popup explanations and some other widgets</li>
<li>Changed object names in preferences window</li>
<li>Fixed local CLI executable making issues with Fedora CI</li>
<li>Fixed theme variant menu in Monet Engine not working with non-english locales</li>
<li>Applied temporary patch for CssProvider.load_from_data() new behavior in GTK 4.10</li>
<li>Translation updates</li>
</ul>
"""

gradience_description = """Gradience is a tool for customizing Libadwaita applications and the adw-gtk3 theme.
The main features of Gradience include the following:

🎨️ Changing any color of Adwaita theme
🖼️ Applying Material 3 color scheme from wallpaper
🎁️ Usage of other users presets
⚙️ Changing advanced options with CSS
🧩️ Extending functionality using plugins"""

# TRANSLATORS: This is a place to put your credits (formats:
# "Name https://example.com" or "Name <email@example.com>",
# no quotes) and is not meant to be translated literally.
translator_credits = """0xMRTT https://github.com/0xMRTT
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
Óscar Fernández Díaz https://github.com/oscfdezdz"""


class GradienceAboutWindow:
    def __init__(self, parent):
        self.parent = parent
        self.app = self.parent.get_application()

        self.setup()

    def setup(self):
        self.about_window = Adw.AboutWindow(
            application_name="Gradience",
            transient_for=self.app.get_active_window(),
            application_icon=constants.app_id,
            developer_name=_("Gradience Team"),
            website=constants.project_url,
            support_url=constants.help_url,
            issue_url=constants.bugtracker_url,
            developers=[
                "0xMRTT https://github.com/0xMRTT",
                "Artyom Fomin https://github.com/ArtyIF",
                "Verantor https://github.com/Verantor",
                "tfuxu https://github.com/tfuxu",
                "u1F98E https://github.com/u1f98e"
            ],
            artists=[
                "David Lapshin https://github.com/daudix-UFO"
            ],
            designers=[
                "David Lapshin https://github.com/daudix-UFO"
            ],
            documenters=[
                "0xMRTT https://github.com/0xMRTT",
                "David Lapshin https://github.com/daudix-UFO"
            ],
            translator_credits=_(translator_credits),
            copyright=_("Copyright © 2022-2023 Gradience Team"),
            license_type=Gtk.License.GPL_3_0,
            version=constants.version,
            release_notes_version=constants.rel_ver,
            release_notes=_(release_notes),
            comments=_(gradience_description),
        )

        self.about_window.add_credit_section(
            _("Plugins by"),
            [
                "0xMRTT https://github.com/0xMRTT",
                "Apisu https://github.com/aspizu",
                "Jonathan Lestrelin https://github.com/jle64"
            ]
        )
        self.about_window.add_credit_section(
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
                "zehkira https://github.com/zehkira"
            ]
        )
        self.about_window.add_credit_section(
            _("Packages by"),
            [
                "0xMRTT https://github.com/0xMRTT",
                "Lyes Saadi https://github.com/lyessaadi"
            ]
        )
        self.about_window.add_credit_section(
            _("Fixes by"),
            [
                "Erick Howard https://github.com/DivineBicycle",
                "Hari Rana https://github.com/TheEvilSkeleton",
                "José Hunter https://github.com/halfmexican",
                "Sabri Ünal https://github.com/libreajans",
                "Sal Watson https://github.com/salarua"
            ]
        )
        self.about_window.add_acknowledgement_section(
            _("Special thanks to"),
            [
                "Artyom Fomin https://github.com/ArtyIF",
                "Weblate https://weblate.org"
            ]
        )

    def show_about(self):
        self.about_window.present()
