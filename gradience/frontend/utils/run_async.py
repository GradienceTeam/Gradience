# run_async.py
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

import sys
import threading
import traceback

from gi.repository import GLib

from gradience.backend.utils.utils import buglog


class RunAsync(threading.Thread):
    def __init__(self, task_func, callback=None, *args, **kwargs):
        self.source_id = None
        if threading.current_thread() is not threading.main_thread():
            raise AssertionError

        super(RunAsync, self).__init__(
            target=self.target, args=args, kwargs=kwargs)

        self.task_func = task_func

        self.callback = callback if callback else lambda r, e: None
        self.daemon = kwargs.pop("daemon", True)

        self.start()

    def target(self, *args, **kwargs):
        result = None
        error = None

        buglog(f"Running async job [{self.task_func}].")

        try:
            result = self.task_func(*args, **kwargs)
        except Exception as exception:
            buglog(
                "Error while running async job: "
                f"{self.task_func}\nException: {exception}"
            )

            error = exception
            _ex_type, _ex_value, trace = sys.exc_info()
            traceback.print_tb(trace)
            traceback_info = "\n".join(traceback.format_tb(trace))

            buglog([str(exception), traceback_info])
        self.source_id = GLib.idle_add(self.callback, result, error)
        return self.source_id
