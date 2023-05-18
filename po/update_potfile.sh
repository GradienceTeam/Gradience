#!/bin/bash
po_dir=$(dirname "$(realpath "$0")")
xgettext -f "$po_dir"/POTFILES -o "$po_dir"/Gradience.pot --add-comments=Translators --keyword=_ --keyword=C_1c,2 --from-code=UTF-8
sed -i "s/SOME DESCRIPTIVE TITLE./Gradience POT file/" "$po_dir"/Gradience.pot
sed -i "s/YEAR THE PACKAGE'S COPYRIGHT HOLDER/$(date +%Y) Gradience Team/" "$po_dir"/Gradience.pot
sed -i "s@same license as the PACKAGE package.@GNU GPLv3 license.@" "$po_dir"/Gradience.pot
sed -i "s/FIRST AUTHOR <EMAIL@ADDRESS>, YEAR./Gradience Team, $(date +%Y)./" "$po_dir"/Gradience.pot

regex="$po_dir/([a-zA-Z_]*).po"
find "$po_dir" -type f -name "*.po" | sed -rn "s:$regex:\1:p" > "$po_dir/LINGUAS"
