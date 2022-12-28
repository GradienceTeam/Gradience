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
import traceback

from gradience.backend.constants import build_type


class Logger(logging.getLoggerClass()):
    """
    This is a wrapper of `logging` module. It provides
    custom formatting for log messages.

    Attributes:
        logger_name (str): Custom name of the logger.
        formatter (dict): Custom formatter for the logger.
    """
    log_colors = {
        "debug": 32,
        "info": 36,
        "warning": 33,
        "error": 31,
        "critical": 41
    }

    log_format = {
        'fmt': '[%(name)s] %(message)s'
    }

    def __set_exc_info(self, exc):
        exc_tb = traceback.extract_tb(exc.__traceback__)
        exc_info = ""

        # \033[1m for bold text
        if len(exc_tb) > 1:
            exc_info += f"\nExc: {exc}\nAt: "
            for i, tb in enumerate(exc_tb):
                if i == len(exc_tb) - 1:
                    exc_info += f"{tb[0]}:{tb[1]}"
                else:
                    exc_info += f"{tb[0]}:{tb[1]}\n    " # Yes, it must have those four spaces at the end
        elif len(exc_tb) == 1:
            exc_info += f"\nExc: {exc}\nAt: {exc_tb[-1][0]}:{exc_tb[-1][1]}"

        return exc_info

    def __set_level_color(self, level: str, message: str):
        if message is not None and "\n" in message:
            message = message.replace("\n", "\n\t")
        color_id = self.log_colors[level]

        return f"\033[1;{color_id}m{level.upper()}:\033[0m {message}"

    def __init__(self, logger_name=None, formatter=None):
        """
        The constructor for Logger class.

        When initializing this class, you should specify a logger name for debugging purposes,
        even if you didn't wrote any debug messages in your code.
        The logger name should usually be a name of your module's main class or module name.
        """
        if formatter is None:
            formatter = self.log_format
        formatter = logging.Formatter(**formatter)

        if logger_name:
            self.root.name = f"Gradience.{logger_name}"
        else:
            self.root.name = "Gradience"

        if build_type == "debug":
            self.root.setLevel(logging.DEBUG)
        else:
            self.root.setLevel(logging.INFO)
        self.root.handlers = []

        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        self.root.addHandler(handler)

    def debug(self, message):
        self.root.debug(self.__set_level_color("debug", str(message)))

    def info(self, message):
        self.root.info(self.__set_level_color("info", str(message)))

    def warning(self, message, exc=None):
        if exc:
            message += self.__set_exc_info(exc)
        self.root.warning(self.__set_level_color("warning", str(message)))

    def error(self, message, exc=None):
        if exc:
            message += self.__set_exc_info(exc)
        self.root.error(self.__set_level_color("error", str(message)))

    def critical(self, message, exc=None):
        if exc:
            message += self.__set_exc_info(exc)
        self.root.critical(self.__set_level_color("critical", str(message)))

    def set_silent(self):
        self.root.handlers = []
