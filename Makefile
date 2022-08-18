python-dep:
	pip install -r requirements.txt
	pip3 install $(shell pwd)/monet/material_color_utilities_python-0.1.0-py3-none-any.whl

global:
	meson builddir --prefix=/usr/local --wipe
	sudo ninja -C builddir install

local:
	meson builddir --wipe
	meson configure builddir -Dprefix="$(shell pwd)/builddir/testdir"
	ninja -C builddir install
	ninja -C builddir run
