install:
	sudo meson builddir --prefix=/usr/local --wipe
	sudo ninja -C builddir install

global:
	sudo meson builddir --prefix=/usr --wipe
	sudo ninja -C builddir install

user:
	meson builddiruser
	meson configure builddiruser -Dprefix="$(pwd)/builddiruser/testdir"
	ninja -C builddiruser install
	ninja -C builddiruser run