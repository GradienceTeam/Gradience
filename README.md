<img align="left" alt="Project logo" src="https://github.com/AdwCustomizerTeam/AdwCustomizer/blob/main/data/icons/hicolor/scalable/apps/com.github.AdwCustomizerTeam.AdwCustomizer.svg" />

# Gradience
Change the look of Adwaita, with ease

![Screenshot of interface with Adwaita light theme](https://github.com/AdwCustomizerTeam/Design/blob/main/Screenshots/main_screenshot.png)

Gradience is a tool for customizing Libadwaita applications and the adw-gtk3 theme.

<details>
  <summary>More screenshots</summary>
  
  ![Screenshot of interface with a customized theme](https://github.com/AdwCustomizerTeam/Design/blob/main/Screenshots/customized_screenshot.png)
  
  ![Screenshot of proof that this actually works](https://github.com/AdwCustomizerTeam/Design/blob/main/Screenshots/proof_of_work_screenshot.png)
</details>

[![Build flatpak](https://github.com/AdwCustomizerTeam/AdwCustomizer/actions/workflows/flatpak.yml/badge.svg)](https://github.com/AdwCustomizerTeam/AdwCustomizer/actions/workflows/flatpak.yml)
[![Build flatpak nightly](https://github.com/AdwCustomizerTeam/AdwCustomizer/actions/workflows/flatpak-nightly.yml/badge.svg)](https://github.com/AdwCustomizerTeam/AdwCustomizer/actions/workflows/flatpak-nightly.yml)
[![Translate on Weblate](https://hosted.weblate.org/widgets/GradienceTeam/-/svg-badge.svg)](https://hosted.weblate.org/projects/GradienceTeam/gradience)
[![Chat on Matrix](https://matrix.to/img/matrix-badge.svg)](https://matrix.to/#/#AdwCustomizer:matrix.org)

## Building and Installing

**[NOTE]** See `next` branch for UI rework and latest commits.

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
pip3 install $(pwd)/monet/material_color_utilities_python-0.1.0-py3-none-any.whl
```

### Global installation:
```sh
git clone https://github.com/AdwCustomizerTeam/AdwCustomizer.git
cd AdwCustomizer
meson builddir --prefix=/usr/local
sudo ninja -C builddir install
```

### Local build (for testing and development purposes):
```sh
git clone https://github.com/AdwCustomizerTeam/AdwCustomizer.git
cd AdwCustomizer
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
- [ ] Add plugin support. Will help integration with others tools.
- [ ] Release on Flathub
- [ ] Full theme preview
- [ ] Customize GNOME Shell
- [ ] Customize GDM
- [ ] Customize KvLibadwaita
- [ ] Customize Firefox GNOME theme

## Contribute
### Code
Fork this repository, then create a push request when you're done adding features or fixing bugs.

### Localize

<a href="https://hosted.weblate.org/engage/GradienceTeam/">
<img src="https://hosted.weblate.org/widgets/GradienceTeam/-/gradience/open-graph.png" alt="Translation status" />
</a>

## About Name

Gradience is originally named Adwaita Manager

Meaning of Gradience is: https://en.wiktionary.org/wiki/gradience

Meaning of an icon is: "A Paint Roller repaints Adwaita window keeping it's functionality"
