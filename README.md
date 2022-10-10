<h1 align="center">
  <img src="https://github.com/GradienceTeam/Gradience/raw/main/data/icons/hicolor/scalable/apps/com.github.GradienceTeam.Gradience.svg" alt="Gradience" width="192" height="192"/>
  <br>
  Gradience
</h1>

<p align="center">
  <strong>Change the look of Adwaita, with ease</strong>
</p>

<p align="center">
  <a href="https://flathub.org/apps/details/com.github.GradienceTeam.Gradience">
    <img width="200" alt="Download on Flathub" src="https://flathub.org/assets/badges/flathub-badge-i-en.svg"/>
  </a>
  <br>
</p>

<br>

<p align="center">
  <a href="https://hosted.weblate.org/engage/GradienceTeam">
    <img alt="Translation status" src="https://hosted.weblate.org/widgets/GradienceTeam/-/svg-badge.svg"/>
  </a>
  <a href="https://github.com/GradienceTeam/Gradience/actions/workflows/CI.yml">
    <img alt="CI status" src="https://github.com/GradienceTeam/Gradience/actions/workflows/CI.yml/badge.svg"/>
  </a>
  <a href="https://flathub.org/apps/details/com.github.GradienceTeam.Gradience">
    <img alt="Flathub downloads" src="https://img.shields.io/badge/dynamic/json?color=informational&label=downloads&logo=flathub&logoColor=white&query=%24.installs_total&url=https%3A%2F%2Fflathub.org%2Fapi%2Fv2%2Fstats%2Fcom.github.GradienceTeam.Gradience"/>
  </a>
  <a href="https://repology.org/project/gradience/versions">
    <img alt="Packaging status" src="https://repology.org/badge/tiny-repos/gradience.svg">
  </a>
</p>

<p align="center">
  <img src="https://github.com/GradienceTeam/Design/raw/main/Screenshots/preview.png" alt="Preview"/>
</p>

Gradience is a tool for customizing Libadwaita applications and the adw-gtk3 theme.

> **Warning**
> [Gradience, stopthemingmy.app and Adwaita Developers](#gradience-stopthemingmyapp-and-adwaita-developers)

The main features of Gradience include the following:

* 🎨️ Changing any color of Adwaita theme
* 🖼️ Applying Material 3 color scheme from wallpaper
* 🎁️ Usage of other users presets
* ⚙️ Changing advanced options with CSS
* 🧩️ Extending functionality using plugins

<details>
  <summary>📷️ More screenshots</summary>
  
  ![Monet Tab](https://github.com/GradienceTeam/Design/raw/main/Screenshots/monet_purple.png)
  
  ![Proof of Work](https://github.com/GradienceTeam/Design/raw/main/Screenshots/proof_purple.png)
</details>


## 🏗️ Building from source

### GNOME Builder

GNOME Builder is the environment used for developing this application.
It can use Flatpak manifests to create a consistent building and running
environment cross-distro. Thus, it is highly recommended you use it.

1. Download [GNOME Builder](https://flathub.org/apps/details/org.gnome.Builder).
2. In Builder, click the "Clone Repository" button at the bottom, using `https://github.com/GradienceTeam/Gradience.git` as the URL.
3. Click the build button at the top once the project is loaded.

### Meson

#### Prerequisites

The following packages are required to build Gradience:

* python3
* python-gobject
* [blueprint-compiler](https://jwestman.pages.gitlab.gnome.org/blueprint-compiler/setup.html)
* gtk4
* libadwaita (>= 1.2)
* meson
* ninja-build

Required Python libraries:

```shell
pip install -r requirements.txt
```

#### Build Instruction

##### Global installation

```shell
git clone https://github.com/GradienceTeam/Gradience.git
cd Gradience
meson builddir --prefix=/usr/local
sudo ninja -C builddir install
```

##### Local build (for testing and development purposes)

```shell
git clone https://github.com/GradienceTeam/Gradience.git
cd Gradience
meson builddir
meson configure builddir -Dprefix="$(pwd)/builddir"
ninja -C builddir install
ninja -C builddir run
```

> **Note** 
> During testing and developement, as a convenience, you can use the `local.sh` script to quickly rebuild local builds.


## 🙌 Contribute to Gradience 

### Code
Fork this repository, then create a push request when you're done adding features or fixing bugs.

### Localisation 

You can help Gradience translate into your native language. If you found any typos
or think you can improve a translation, you can use the [Weblate](https://hosted.weblate.org/engage/GradienceTeam) platform.

[![Translations](https://hosted.weblate.org/widgets/GradienceTeam/-/horizontal-auto.svg)](https://hosted.weblate.org/engage/GradienceTeam)


## ✨️ Contributors

[![Contributors](https://contrib.rocks/image?repo=GradienceTeam/Gradience)](https://github.com/GradienceTeam/Gradience/graphs/contributors)


## 🏷️ About the Name

Gradience was originally named Adwaita Manager.

You can see the meaning of Gradience on [Wiktionary](https://en.wiktionary.org/wiki/gradience).

The icon represents: _A Paint Roller repainting an Adwaita window, keeping it's functionality._

## 🌱️ Gradience, [stopthemingmy.app](https://stopthemingmy.app) and Adwaita Developers

Gradience Team is not against [stopthemingmy.app](https://stopthemingmy.app) and Adwaita Developers idea, Gradience is a tool for tinkers that want to theme their desktops at their liking, and not a tool for distributions to change theme in them by default, Gradience Team agrees with importance of unified look of Adwaita to make sure that all apps work right and Developers have unified and stable tool for creating their apps.

## 💝 Acknowledgment

Original author of Gradience is [Artyom Fomin](https://github.com/ArtyIF), now it developed by [Gradience Team](https://github.com/GradienceTeam)

This README is based on README from [Kooha](https://github.com/SeaDve/Kooha) by [Dave Patrick Caberto](https://github.com/SeaDve)
