# logger.py
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

import logging

from gradience.backend.constants import build_type


class Logger(logging.getLoggerClass()):
    """
    This is a wrapper of `logging` module. It provides
    custom formatting for log messages.
    """
    log_colors = {
        "debug": 37,
        "info": 36,
        "warning": 33,
        "error": 31,
        "critical": 41
    }

    log_format = {
        'fmt': '\033[1m[%(levelname)s]\033[0m [%(name)s] %(message)s'
    }

    def __set_color(self, level, message: str):
        if message is not None and "\n" in message:
            message = message.replace("\n", "\n\t") + "\n"
        color_id = self.log_colors[level]
        return "\033[%dm%s\033[0m" % (color_id, message)

    def __init__(self, formatter=None):
        if formatter is None:
            formatter = self.log_format
        formatter = logging.Formatter(**formatter)

        self.root.name = "gradience"

        if build_type == "debug":
            self.root.setLevel(logging.DEBUG)
        else:
            self.root.setLevel(logging.INFO)
        self.root.handlers = []

        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        self.root.addHandler(handler)

    def debug(self, message, **kwargs):
        self.root.debug(self.__set_color("debug", str(message)), )

    def info(self, message, **kwargs):
        self.root.info(self.__set_color("info", str(message)), )

    def warning(self, message, **kwargs):
        self.root.warning(self.__set_color("warning", str(message)),)

    def error(self, message, **kwargs):
        self.root.error(self.__set_color("error", str(message)), )

    def critical(self, message, **kwargs):
        self.root.critical(self.__set_color("critical", str(message)), )

    def set_silent(self):
        self.root.handlers = []
