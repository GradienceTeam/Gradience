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
import signal

from gi.repository import GLib, Gio

from gradience.backend.logger import Logger

logging = Logger(logger_name="GradienceSubprocess")


# TODO: Check how Dev Toolbox has its backend done fully in async using Gio.Task.
# Example: https://github.com/aleiepure/devtoolbox/blob/main/src/services/gzip_compressor.py
class GradienceSubprocess:
    """
    Wrapper for Gio's Subprocess class to provide easy to use
    asynchronous process spawning and stdout data retrievement.

    Documentation: https://docs.gtk.org/gio/class.Subprocess.html
    """

    def __init__(self):
        self.cancellable = Gio.Cancellable()

        self.priority = GLib.PRIORITY_DEFAULT
        self.flags = Gio.SubprocessFlags.STDOUT_PIPE

        self.data_array = None

    def get_cancellable(self) -> Gio.Cancellable:
        return self._cancellable

    def run(
        self, callback: callable, command: list, allow_escaping: bool = False
    ) -> None:
        """
        Spawns asynchronously a new child process (subprocess) using Gio's Subprocess class.

        Put custom function as a `callback` parameter to receive a signal
        after a subprocess is finished.

        You can enable executing commands outside Flatpak sandbox by enabling
        `allow_escaping` parameter.
        """
        self.finish_callback = callback

        if allow_escaping and os.environ.get("FLATPAK_ID"):
            command = ["flatpak-spawn", "--host"] + command

        logging.debug(f"Spawning: {command}")

        try:
            self.process = Gio.Subprocess.new(command, self.flags)

            self.process.wait_check_async(
                cancellable=self.cancellable, callback=self._on_finished
            )

            self.stream = self.process.get_stdout_pipe()
            self.data_stream = Gio.DataInputStream.new(self.stream)

            self.queue_read()
        except GLib.GError as e:
            logging.error("Failed to execute an external process.", exc=e)

    def get_stdout_pipe(self) -> Gio.InputStream:
        """
        Returns stdout stream as a Gio.InputStream object.

        Documentation: https://docs.gtk.org/gio/class.InputStream.html
        """
        return self.stream

    def get_stdout_data(self, decode=False) -> str or bytes:
        """
        Returns a data retrieved from stdout stream.

        Default behavior returns a full data collection in bytes array.
        Setting `decode` parameter to True will automatically decode data to string object.
        """
        if decode:
            stdout_string = self.data_array[0].decode()
            return stdout_string

        return self.data_array[0]

    def queue_read(self) -> None:
        self.data_stream.read_line_async(
            io_priority=self.priority,
            cancellable=self.cancellable,
            callback=self._on_data,
        )

    def cancel_read(self) -> None:
        self.cancellable.cancel()

    def _on_finished(self, process, result) -> None:
        try:
            process.wait_check_finish(result)
        except GLib.GError:
            raise

        self.cancel_read()

        logging.debug("Process finished successfully")

        if self.finish_callback:
            self.finish_callback(self)

    def _on_data(self, stream, result) -> None:
        try:
            self.data_array = stream.read_line_finish(result)
        except GLib.GError as e:
            logging.error("Failed to asynchronously read stdout stream data.", exc=e)
            raise

    def stop(self) -> None:
        logging.debug(f"Terminating process, ID {self.process.get_identifier()}")
        self.process.send_signal(signal.SIGTERM)

    def kill(self) -> None:
        logging.debug(f"Killing process, ID {self.process.get_identifier()}")
        self.cancel_read()
        self.process.send_signal(signal.SIGKILL)


# NOTE: For testing purposes only.
# TODO: Remove later
if __name__ == "__main__":
    priority = GLib.PRIORITY_DEFAULT
    subprocess = GradienceSubprocess()
    mainloop = GLib.MainLoop()

    GLib.idle_add(subprocess.run, ["gnome-shell", "--version"])
    GLib.timeout_add_seconds(priority=priority, interval=5, function=mainloop.quit)
    # GLib.timeout_add_seconds(priority=priority, interval=5, function=print(subprocess.get_stdout_data(True)))
    mainloop.run()
