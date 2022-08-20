<img align="left" alt="Project logo" src="https://github.com/GradienceTeam/Gradience/blob/main/data/icons/hicolor/scalable/apps/com.github.GradienceTeam.Gradience.svg" />
<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-3-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->

# Gradience
Change the look of Adwaita, with ease

![Screenshot of interface with Adwaita light theme](https://github.com/GradienceTeam/Design/blob/main/Screenshots/main_screenshot.png)

Gradience is a tool for customizing Libadwaita applications and the adw-gtk3 theme.

<details>
  <summary>More screenshots</summary>
  
  ![Screenshot of interface of Monet Tab](https://github.com/GradienceTeam/Design/blob/main/Screenshots/monet_purple.png)
  
  ![Screenshot of proof that this actually works](https://github.com/GradienceTeam/Design/blob/main/Screenshots/proof_of_work_screenshot.png)
</details>

[![Build flatpak](https://github.com/GradienceTeam/Gradience/actions/workflows/flatpak.yml/badge.svg)](https://github.com/GradienceTeam/Gradience/actions/workflows/flatpak.yml)
[![Build flatpak nightly](https://github.com/GradienceTeam/Gradience/actions/workflows/flatpak-nightly.yml/badge.svg)](https://github.com/GradienceTeam/Gradience/actions/workflows/flatpak-nightly.yml)
[![Translate on Weblate](https://hosted.weblate.org/widgets/GradienceTeam/-/svg-badge.svg)](https://hosted.weblate.org/engage/GradienceTeam)
[![Chat on Matrix](https://matrix.to/img/matrix-badge.svg)](https://matrix.to/#/#Gradience:matrix.org)

## Building and Installing

**[NOTE]** See `next` branch for latest commits.

## Requirements:
- Python 3 `python`
- PyGObject `python-gobject`
- Blueprint <code>[blueprint-compiler](https://jwestman.pages.gitlab.gnome.org/blueprint-compiler/setup.html)</code>
- GTK4 `gtk4`
- libadwaita (>= 1.2.alpha) `libadwaita`
- Meson `meson`
- Ninja `ninja`

## Building from source:

Install required Python libraries:
```sh
pip install -r requirements.txt
```

### Global installation:
```sh
git clone https://github.com/GradienceTeam/Gradience.git
cd Gradience
meson builddir --prefix=/usr/local
sudo ninja -C builddir install
```

### Local build (for testing and development purposes):
```sh
git clone https://github.com/GradienceTeam/Gradience.git
cd Gradience
meson builddir
meson configure builddir -Dprefix="$(pwd)/builddir/testdir"
ninja -C builddir install
ninja -C builddir run
```

**[NOTE]** During testing and developement, as a convenience, you can use the `local.sh` script to quickly rebuild local builds.

### Building using flatpak-builder:

1. Open Terminal
2. Run `git clone https://github.com/GradienceTeam/Gradience.git && cd Gradience`
3. Add the `gnome-nightly` Flatpak repository `flatpak remote-add --if-not-exists gnome-nightly https://nightly.gnome.org/gnome-nightly.flatpakrepo`
4. Install the `master` version of GNOME SDK: `flatpak install org.gnome.Sdk/x86_64/master org.gnome.Platform/x86_64/master`
5. Run `flatpak-builder --install --user --force-clean repo/ com.github.GradienceTeam.Gradience.json`

Alternatively, open the project with GNOME Builder, then build and run it.

## Setup Tutorial

### Libadwaita applications
No additional setup is required for native Libadwaita applications.

For Flatpak Libadwaita applications, you need to override their permissions:
- Run `sudo flatpak override --filesystem=xdg-config/gtk-4.0` or
- Use [Flatseal](https://github.com/tchx84/Flatseal) and adding `xdg-config/gtk-4.0` to **Other files** in the **Filesystem** section of **All Applications**

### Vanilla GTK 4 applications
Use [this guide](https://github.com/lassekongo83/adw-gtk3/blob/main/gtk4.md) to theme vanilla GTK 4 applications.

### GTK 3 applications
- Install and apply the [adw-gtk3](https://github.com/lassekongo83/adw-gtk3#readme) theme (don't forget to install the Flatpak package!)
- For Flatpak applications, you need to override their permissions:
  - Run `sudo flatpak override --filesystem=xdg-config/gtk-3.0` or
  - Use [Flatseal](https://github.com/tchx84/Flatseal) and adding `xdg-config/gtk-3.0` to **Other files** in the **Filesystem** section of **All Applications**

## Roadmap
This tool is currently WIP, but it already has a plenty of features and is very usable. Below is the roadmap, where all the checked features are already implemented:

- [x] Customize named colors, either with a color picker or with text
- [x] Explanations for some named colors
- [x] Partial theme preview
- [x] Built-in presets for Adwaita and Adwaita Dark (based on default libadwaita colors)
- [x] Apply changes to libadwaita, GTK4 (with extracted libadwaita theme) and GTK3 (with the adw-gtk3 theme) applications
- [x] Load and create custom presets
- [x] View adw-gtk3's support of variables
- [x] View parsing errors
- [x] Customize palette colors
- [x] Add custom CSS code
- [x] Localization support
- [x] Normalize color variables
- [x] Make the code more secure
- [ ] Add plugin support. Will help integration with others tools. (WIP)
- [ ] Release on Flathub
- [ ] Full theme preview
- [ ] Customize GNOME Shell
- [ ] Customize GDM
- [ ] Customize KvLibadwaita
- [ ] Customize Firefox GNOME theme

## Contribute
### Code
Fork this repository, then create a push request when you're done adding features or fixing bugs.

### Localisation 

[![Translations](https://hosted.weblate.org/widgets/GradienceTeam/-/multi-auto.svg)](https://hosted.weblate.org/engage/GradienceTeam)

## About Name

Gradience is originally named Adwaita Manager

Meaning of Gradience is: https://en.wiktionary.org/wiki/gradience

Meaning of an icon is: "A Paint Roller repaints Adwaita window keeping it's functionality"

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="https://github.com/rene-coty"><img src="https://avatars.githubusercontent.com/u/95506494?v=4?s=100" width="100px;" alt=""/><br /><sub><b>rene-coty</b></sub></a><br /><a href="#translation-rene-coty" title="Translation">🌍</a></td>
    <td align="center"><a href="https://github.com/0xMRTT"><img src="https://avatars.githubusercontent.com/u/105598867?v=4?s=100" width="100px;" alt=""/><br /><sub><b>0xMRTT</b></sub></a><br /><a href="#maintenance-0xMRTT" title="Maintenance">🚧</a> <a href="#translation-0xMRTT" title="Translation">🌍</a> <a href="https://github.com/GradienceTeam/Gradience/commits?author=0xMRTT" title="Code">💻</a></td>
    <td align="center"><a href="https://linktr.ee/daudix_ufo"><img src="https://avatars.githubusercontent.com/u/77155297?v=4?s=100" width="100px;" alt=""/><br /><sub><b>David Lapshin</b></sub></a><br /><a href="#translation-daudix-UFO" title="Translation">🌍</a></td>
  </tr>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!