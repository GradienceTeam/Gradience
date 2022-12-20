# monet.py
#
# Change the look of Adwaita, with ease
# Copyright (C) 2022 Gradience Team
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

import os

from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
import material_color_utilities_python as monet

from gradience.backend.models.preset import Preset

from gradience.backend.logger import Logger

logging = Logger()


class Monet:
    def __init__(self):
        self.palette = None

    def generate_from_image(self, image_path: str) -> dict:
        if image_path.endswith(".svg"):
            drawing = svg2rlg(image_path)
            image_path = os.path.join(
                os.environ.get("XDG_RUNTIME_DIR"), "gradience_bg.png"
            )
            renderPM.drawToFile(drawing, image_path, fmt="PNG")

        if image_path.endswith(".xml"):
            logging.error(f"XML files are unsupported by Gradience's Monet implementation.")
            return False

        try:
            monet_img = monet.Image.open(image_path)
        except Exception as e:
            logging.error(f"An error occurred while generating a Monet palette. Exc: {e}")
            return False
        else:
            basewidth = 64
            wpercent = basewidth / float(monet_img.size[0])
            hsize = int((float(monet_img.size[1]) * float(wpercent)))
            monet_img = monet_img.resize(
                (basewidth, hsize), monet.Image.Resampling.LANCZOS
            )

            self.palette = monet.themeFromImage(monet_img)

        return self.palette
