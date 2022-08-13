#!/usr/bin/bash

read -p "Do you want to install Python requirements? (yes, no): " answer

if [[ "$answer" == "yes" ]]; then
    pip3 install --user -r requirements.txt
    pip3 install $(pwd)/monet/material_color_utilities_python-0.1.0-py3-none-any.whl
elif [[ "$answer" == "no" ]]; then
    echo "Skipping requirements installation"
fi

echo "Cleaning builddir directory"
rm -r builddir

echo "Rebuilding"
meson builddir
meson configure builddir -Dprefix="$(pwd)/builddir/testdir"
ninja -C builddir install

echo "Running"
ninja -C builddir run