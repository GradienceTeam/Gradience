# Maintainer: Igor Dyatlov <dyatlov.igor@protonmail.com>

pkgname=gradience-git
_pkgname=Gradience
pkgver=r1043.78bda9d
pkgrel=1
pkgdesc="Change the look of Adwaita, with ease"
arch=('x86_64')
url="https://github.com/GradienceTeam/Gradience"
license=('GPL3')
depends=('libadwaita-git>=1.2.alpha' 'python-gobject' 'python-anyascii' 'python-pillow' 'python-pluggy' 'python-svglib' 'python-urllib3' 'python-regex' 'python-material-color-utilities' 'libportal-gtk4')
makedepends=('git' 'meson' 'blueprint-compiler' 'gobject-introspection')
checkdepends=('appstream-glib')
optdepends=('adw-gtk3: The theme from libadwaita ported to GTK-3'
            'adw-gtk-theme: LibAdwaita Theme for all GTK3 and GTK4 Apps.')
provides=("${pkgname%-git}")
conflicts=("${pkgname%-git}" adwcustomizer-git)
install='xdg-config.install'
source=(git+$url.git)
b2sums=('SKIP')

pkgver() {
  cd "${_pkgname%-git}"
  ( set -o pipefail
    git describe --long 2>/dev/null | sed 's/^v//;s/\([^-]*-g\)/r\1/;s/-/./g' ||
    printf "r%s.%s" "$(git rev-list --count HEAD)" "$(git rev-parse --short HEAD)"
  )
}

build() {
  arch-meson "${_pkgname%-git}" build
  meson compile -C build
}

check() {
  meson test -C build || :
}

package() {
  meson install -C build --destdir "$pkgdir"
}
