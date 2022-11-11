install:
	sudo meson setup builddir --prefix=/usr/local --wipe
	sudo ninja -C builddir install

global:
	sudo meson setup builddir --prefix=/usr --wipe
	sudo ninja -C builddir install

release:
	sudo meson setup builddir --prefix=/usr --Dbuildtype=release --wipe
	sudo ninja -C builddir install

user:
	meson setup builddir --prefix="$(shell pwd)/builddir" --buildtype=debug --wipe
	ninja -C builddir install
	ninja -C builddir run
