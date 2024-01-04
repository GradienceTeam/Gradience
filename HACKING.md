## 🙌 Contribute to Gradience

### Code

Fork this repository, then create a push request when you're done adding features or fixing bugs.

### Localization

You can help Gradience translate into your native language. If you found any typos
or think you can improve a translation, you can use the [Weblate](https://hosted.weblate.org/engage/GradienceTeam) platform.

[![Translation status](https://hosted.weblate.org/widgets/GradienceTeam/-/multi-auto.svg)](https://hosted.weblate.org/engage/GradienceTeam)


## 🏗️ Building from source

### GNOME Builder

GNOME Builder is the environment used for developing this application.
It can use Flatpak manifests to create a consistent building and running
environment cross-distro. Thus, it is highly recommended you use it.

1. Download [GNOME Builder](https://flathub.org/apps/details/org.gnome.Builder).
2. In Builder, click the "Clone Repository" button at the bottom, using `https://github.com/GradienceTeam/Gradience.git` as the URL.
3. Click the build button at the top once the project is loaded.

### Flatpak Builder

`flatpak-builder` is a wrapper around the `flatpak build` command that automates the building of applications and their dependencies.
It uses Flatpak manifests to download and pack needed dependencies with compiled program into a single Flatpak image that can be later distributed or installed on your system. We recommend this method if you have problems with GNOME Builder.

#### Prerequisites

- Flatpak Builder `flatpak-builder`
- GNOME SDK runtime `org.gnome.Sdk//44`
- GNOME Platform runtime `org.gnome.Platform//44`

Install required runtimes:
```shell
flatpak install org.gnome.Sdk//44 org.gnome.Platform//44
```

#### Build Instruction

##### User installation
```shell
git clone https://github.com/GradienceTeam/Gradience.git
cd Gradience
git submodule update --init --recursive
flatpak-builder --install --user --force-clean repo/ build-aux/flatpak/com.github.GradienceTeam.Gradience.json
```

##### System installation
```shell
git clone https://github.com/GradienceTeam/Gradience.git
cd Gradience
git submodule update --init --recursive
flatpak-builder --install --system --force-clean repo/ build-aux/flatpak/com.github.GradienceTeam.Gradience.json
```

### Meson

#### Prerequisites

The following packages are required to build Gradience:

- Python 3 `python`
- PyGObject `python-gobject`
- Blueprint [`blueprint-compiler`](https://jwestman.pages.gitlab.gnome.org/blueprint-compiler/setup.html)
- GTK 4 `gtk4`
- Libadwaita (>= 1.2.alpha) `libadwaita`
- Libsoup 3 (>= 3.2.0) `libsoup`
- Meson `meson`
- Ninja `ninja-build`

Required Python libraries:

```shell
pip install -r requirements.txt
```

#### Build Instruction

##### Global installation

```shell
git clone https://github.com/GradienceTeam/Gradience.git
cd Gradience
git submodule update --init --recursive
meson setup builddir
meson configure builddir -Dprefix=/usr/local
sudo ninja -C builddir install
```

##### Local build (for testing and development purposes)

```shell
git clone https://github.com/GradienceTeam/Gradience.git
cd Gradience
git submodule update --init --recursive
meson setup builddir
meson configure builddir -Dprefix="$(pwd)/builddir"
ninja -C builddir install
ninja -C builddir run
```

> **Note** 
> During testing and development, as a convenience, you can use the `local.sh` script to quickly rebuild local builds.
> If you want to use CLI in local builds, you should type: `./local_cli.sh <command>` instead of `gradience-cli`.

