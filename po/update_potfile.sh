#!/bin/bash
po_dir=$(dirname "$(realpath "$0")")
xgettext -f "$po_dir"/POTFILES -o "$po_dir"/AdwCustomizer.pot --add-comments=Translators --keyword=_ --keyword=C_1c,2 --from-code=UTF-8