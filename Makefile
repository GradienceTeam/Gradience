install:
	sudo meson builddir --prefix=/usr/local --wipe
	sudo ninja -C builddir install

global:
	sudo meson builddir --prefix=/usr --wipe
	sudo ninja -C builddir install

user:
	meson builddir --prefix="$(shell pwd)/builddir/testdir" --wipe
	ninja -C builddir install
	ninja -C builddir run