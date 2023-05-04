# subprocess.py
#
# Change the look of Adwaita, with ease
# Copyright (C) 2022-2023, Gradience Team
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
#import signal

from typing import Union

import subprocess
from subprocess import SubprocessError, CompletedProcess

from gradience.backend.logger import Logger

logging = Logger(logger_name="GradienceSubprocess")


# TODO: Check how Dev Toolbox has its backend done fully in async using Gio.Task.
# Example: https://github.com/aleiepure/devtoolbox/blob/main/src/services/gzip_compressor.py
# TODO: Replace subprocess.run() with subprocess.Popen() for more control over subprocesses
class GradienceSubprocess:
    """
    Wrapper for Python's `subprocess` module to provide an easy to use
    synchronous process spawning and stdout data retrievement with support
    for Flatpak sandbox escape.

    Documentation: https://docs.python.org/3/library/subprocess.html
    """

    def __init__(self):
        pass

    def run(self, command: list, timeout: int = None, allow_escaping: bool = False) -> CompletedProcess:
        """
        Spawns synchronously a new child process (subprocess) using Python's `subprocess` module.

        You can set the `timeout` parameter to kill the process after a
        specified amount of seconds.

        You can enable executing commands outside Flatpak sandbox by
        enabling `allow_escaping` parameter.
        """

        if allow_escaping and os.environ.get('FLATPAK_ID'):
            command = ['flatpak-spawn', '--host'] + command

        logging.debug(f"Spawning: {command}")

        try:
            process = subprocess.run(command, check=True,
                            capture_output=True, timeout=timeout)
        except SubprocessError:
            raise
        except FileNotFoundError:
            raise

        return process

    def get_stdout_data(self, process: CompletedProcess, decode: bool = False) -> Union[str, bytes]:
        """
        Returns a data retrieved from stdout stream.

        Default behavior returns a full data collection in bytes array.
        Setting ``decode`` parameter to True will automatically decode data to string object.
        """

        if decode:
            stdout_string = process.stdout.decode()
            return stdout_string

        return process.stdout

    '''def stop(self, process: CompletedProcess) -> None:
        logging.debug(f"Terminating process, ID {process.get_identifier()}")
        process.send_signal(signal.SIGTERM)

    def kill(self, process: CompletedProcess) -> None:
        logging.debug(f"Killing process, ID {process.get_identifier()}")
        self.cancel_read()
        process.send_signal(signal.SIGKILL)'''
