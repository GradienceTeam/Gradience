> **Warning**
> This software is currently in a **beta** state. It can break things, and it doesn't yet have a polished, _foolproof_ UX.
>
> Contributions are welcome!
>
> Please, if you got into some trouble with it, just create a [new issue](https://github.com/GradienceTeam/Gradience/issues/new?assignees=&labels=type%2Fbug&template=bug_report.yml&title=bug%3A+), or contact us on [Matrix](https://matrix.to/#/#Gradience:matrix.org) and [Discord](https://discord.com/invite/4njFDtfGEZ).

<h1 align="center">
  <img src="data/icons/hicolor/scalable/apps/com.github.GradienceTeam.Gradience.svg" alt="Gradience" width="192" height="192"/>
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
  <a href="https://github.com/GradienceTeam/Gradience/actions/workflows/build.yml">
    <img alt="Build status" src="https://github.com/GradienceTeam/Gradience/actions/workflows/build.yml/badge.svg"/>
  </a>
  <a href="https://flathub.org/apps/details/com.github.GradienceTeam.Gradience">
    <img alt="Flathub downloads" src="https://img.shields.io/badge/dynamic/json?color=informational&label=downloads&logo=flathub&logoColor=white&query=%24.installs_total&url=https%3A%2F%2Fflathub.org%2Fapi%2Fv2%2Fstats%2Fcom.github.GradienceTeam.Gradience"/>
  </a>
  <a href="https://repology.org/project/gradience/versions">
    <img alt="Packaging status" src="https://repology.org/badge/tiny-repos/gradience.svg">
  </a>
</p>

<p align="center">
  <a href="https://matrix.to/#/#Gradience:matrix.org">
    <img alt="Chat on Matrix" src="https://img.shields.io/matrix/Gradience:matrix.org?color=%230dbd8b&label=Gradience&logo=matrix&logoColor=white"/>
  </a>
  <a href="https://discord.com/invite/4njFDtfGEZ">
    <img alt="Chat on Discord" src="https://dcbadge.vercel.app/api/server/4njFDtfGEZ?style=flat&theme=default-inverted"/>
  </a>
</p>

<p align="center">
  <a href="https://stopthemingmy.app">
    <img alt="Please do not theme this app" src="https://stopthemingmy.app/badge.svg"/>
  </a>
</p>

<p align="center">
  <img src="https://github.com/GradienceTeam/Design/raw/main/Covers/preview.png" alt="Preview"/>
</p>

Gradience is a tool for customizing Libadwaita applications and the adw-gtk3 theme.

> **Warning**
> [Gradience, stopthemingmy.app and Adwaita Developers](#%EF%B8%8F-gradience-stopthemingmyapp-and-adwaita-developers)

The main features of Gradience include the following:

- 🎨️ Changing any color of Adwaita theme
- 🖼️ Applying Material 3 color scheme from wallpaper
- 🎁️ Usage of other users presets
- ⚙️ Changing advanced options with CSS
- 🧩️ Extending functionality using plugins

<details>
  <summary>📷️ More screenshots</summary>

  ![Monet Tab](https://github.com/GradienceTeam/Design/raw/main/Screenshots/monet_purple.png)

  ![Proof of Work](https://github.com/GradienceTeam/Design/raw/main/Screenshots/proof_purple.png)
</details>


## 🎨️ Theming setup

> **Note**
> You can go to `Preferences` and apply overrides for Flatpak

<details>
  <summary>🪛️ Manual setup</summary>

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

</details>


## 🔄 Revert Theming

> **Note**
> You can press on the menu button in the headerbar and press `Reset Applied Color Scheme`
> ![Main Gradience menu](https://raw.githubusercontent.com/GradienceTeam/Design/main/Screenshots/hamburger_menu.png)

<details>
  <summary>🪛️ Manual revert</summary>

### Remove GTK 3 and GTK 4 configs

- Run `rm -rf .config/gtk-4.0 .config/gtk-3.0`

### Remove adw-gtk3 theme

- Run `flatpak uninstall adw-gtk3` to remove Flatpak adw-gtk3 theme
- Run `rm -rf .themes/adw-gtk3 .themes/adw-gtk3-dark .local/share/themes/adw-gtk3 .local/share/themes/adw-gtk3-dark` to remove local adw-gtk3 theme

### Reset Flatpak overrides

- Run `sudo flatpak override --reset`

> **Warning**
> This will reset all Flatpak overrides, such as Firefox Wayland override

</details>


## 📦️ Alternative installation methods

> **Warning**
> The main installation method is Flatpak from Flathub

> **Note**
> There are number of Gradience packages that are not tested by Gradience Team and not listed here, available at [Repology](https://repology.org/project/gradience/versions)

### Fedora (COPR)

Gradience is available for Fedora via COPR:

```shell
dnf copr enable lyessaadi/gradience
dnf install gradience
```

### Debian (And derivatives)

> **Warning**
> Not available yet.

### Arch Linux (AUR)

Gradience is available for Arch Linux via AUR:

Using [Paru](https://github.com/morganamilo/paru):

```shell
paru -S gradience
```

For latest changes:

```shell
paru -S gradience-git
```

<details>
  <summary>🪛️ Without AUR helpers</summary>

```shell
git clone https://aur.archlinux.org/gradience.git
cd gradience
makepkg -sic
```

For latest changes:

```shell
git clone https://aur.archlinux.org/gradience-git.git
cd gradience-git
makepkg -sic
```

</details>

### NixOS

> **Warning**
> It's currently only available in `unstable`

Gradience is available for NixOS:

```shell
nix-shell -p gradience
```


## 🏗️ Building from source

### GNOME Builder

GNOME Builder is the environment used for developing this application.
It can use Flatpak manifests to create a consistent building and running
environment cross-distro. Thus, it is highly recommended you use it.

1. Download [GNOME Builder](https://flathub.org/apps/details/org.gnome.Builder).
2. In Builder, click the "Clone Repository" button at the bottom, using `https://github.com/GradienceTeam/Gradience.git` as the URL.
3. Click the build button at the top once the project is loaded.

For more building and installation methods, see [HACKING.md](HACKING.md)


## 🎛️ Miscellaneous

### Show welcome window again

The following command will make Gradience show welcome screen on next launch, like you just installed it

#### Flatpak

```shell
flatpak run --command=gsettings com.github.GradienceTeam.Gradience reset com.github.GradienceTeam.Gradience first-run
```

#### Alternative installation methods

```shell
gsettings reset com.github.GradienceTeam.Gradience first-run
```


## ℹ️ FAQ

### How can I launch a CLI?
Refer to [temporary CLI documentation](https://github.com/GradienceTeam/Gradience/wiki/Using-CLI) in repo's wiki for instructions on how to launch a CLI.


## 🙌 Contribute to Gradience

See [HACKING.md](HACKING.md)


## ✨️ Contributors

[![Contributors](https://contrib.rocks/image?repo=GradienceTeam/Gradience)](https://github.com/GradienceTeam/Gradience/graphs/contributors)


## 🏷️ About the Name

Gradience was originally named Adwaita Manager.

You can see the meaning of Gradience on [Wiktionary](https://en.wiktionary.org/wiki/gradience).

The icon represents: _A Paint Roller repainting an Adwaita window, keeping its functionality._

##  🖌️ About the "Pretty Purple"

The Pretty Purple theme comes from the very beginning, directly from the original author of Gradience, [Artyom Fomin](https://github.com/ArtyIF).

It were called "Purple Guy", presumably as a reference to the FNaF. later it were renamed to Pretty Purple.

Pretty Purple preset were originally shared in the https://github.com/GradienceTeam/Gradience/discussions/23.

Pretty Purple is built-in in the Gradience and used in all Gradience artworks.


## 🌱️ Gradience, [stopthemingmy.app](https://stopthemingmy.app) and Adwaita Developers

> See [gradienceisahack.github.io](https://gradienceisahack.github.io/)

Gradience Team is not against [stopthemingmy.app](https://stopthemingmy.app) and Adwaita Developers idea, Gradience is a tool for tinkers that want to theme their desktops at their liking, and not a tool for distributions to change theme in them by default, Gradience Team agrees with importance of unified look of Adwaita to make sure that all apps work right and Developers have unified and stable tool for creating their apps.


## 💝 Acknowledgment

Special thanks to:

- Original author of Gradience, [Artyom Fomin](https://github.com/ArtyIF) for creating this project
- [Weblate](https://weblate.org) for providing translation platform

This README is based on README from [Kooha](https://github.com/SeaDve/Kooha) by [Dave Patrick Caberto](https://github.com/SeaDve)
