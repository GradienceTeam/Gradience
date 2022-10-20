from .constants import (
    rootdir,
    app_id,
    rel_ver,
    version,
    bugtracker_url,
    help_url,
    project_url,
)

from gi.repository import Gtk, Adw

APPLICATION_NAME = _("Gradience")
DEVELOPER_NAME = _("Gradience Team")
DEVELOPERS = [
    "0xMRTT https://github.com/0xMRTT",
    "Artyom Fomin https://github.com/ArtyIF",
    "Verantor https://github.com/Verantor",
    "tfuxu https://github.com/tfuxu",
    "u1F98E https://github.com/u1f98e",
]

DOCUMENTERS = [
    "0xMRTT https://github.com/0xMRTT",
    "David Lapshin https://github.com/daudix-UFO"
]

ARTISTS = ["David Lapshin https://github.com/daudix-UFO"]
DESIGNERS = ["David Lapshin https://github.com/daudix-UFO"]

TRANSLATORS = """0xMRTT https://github.com/0xMRTT
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

RELEASE_NOTES = _(
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
)

COMMENTS = _(
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
)

PLUGINS = [
    "0xMRTT https://github.com/0xMRTT",
    "Apisu https://github.com/aspizu",
]

PRESETS = [
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
]

PACKAGERS = [
    "0xMRTT https://github.com/0xMRTT",
    "Lyes Saaudi https://github.com/lyessaadi",
],

FIXES = [
    "Erick Howard https://github.com/DivineBicycle",
    "Hari Rana https://github.com/TheEvilSkeleton",
    "José Hunter https://github.com/halfmexican",
    "Sabri Ünal https://github.com/libreajans",
    "Sal Watson https://github.com/salarua",
],

THANKS = [
    "Artyom Fomin https://github.com/ArtyIF",
    "Weblate https://weblate.org",
]

COPYRIGHT = "© 2022 Gradience Team"


def show_about(window):
    about = Adw.AboutWindow(
        transient_for=window,
        application_name=APPLICATION_NAME,
        application_icon=app_id,
        developer_name=DEVELOPER_NAME,
        website=project_url,
        support_url=help_url,
        issue_url=bugtracker_url,
        developers=DEVELOPERS,
        artists=ARTISTS,
        designers=DESIGNERS,
        documenters=DOCUMENTERS,
        # Translators: This is a place to put your credits (formats:
        # "Name https://example.com" or "Name <email@example.com>",
        # no quotes) and is not meant to be translated literally.
        translator_credits=TRANSLATORS,
        copyright=COPYRIGHT,
        license_type=Gtk.License.GPL_3_0,
        version=version,
        release_notes_version=rel_ver,
        release_notes=RELEASE_NOTES,
        comments=COMMENTS,
    )
    about.add_credit_section(
        _("Plugins by"),
        PLUGINS,
    )
    about.add_credit_section(
        _("Presets by"),
        PRESETS,
    )
    about.add_credit_section(
        _("Packages by"),
        PACKAGERS,
    )
    about.add_credit_section(
        _("Fixes by"),
        FIXES,
    )
    about.add_acknowledgement_section(
        _("Special thanks to"),
        THANKS,
    )

    about.present()
