#!/usr/bin/env python3

import os
import subprocess

build_root = os.environ.get('MESON_BUILD_ROOT')
source_root = os.environ.get('MESON_SOURCE_ROOT')

subprocess.call(['mv', build_root, 'gradience/constants.py', source_root, 'gradience/constants.py'])
