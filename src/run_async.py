
import os
import sys
import threading
import traceback

from gi.repository import GLib

class RunAsync(threading.Thread):
    def __init__(self, task_func, callback=None, *args, **kwargs):
        self.source_id = None
        assert threading.current_thread() is threading.main_thread()

        super(RunAsync, self).__init__(
            target=self.target, args=args, kwargs=kwargs)

        self.task_func = task_func

        self.callback = callback if callback else lambda r, e: None
        self.daemon = kwargs.pop("daemon", True)

        self.start()

    def target(self, *args, **kwargs):
        result = None
        error = None

        print(f"Running async job [{self.task_func}].")

        try:
            result = self.task_func(*args, **kwargs)
        except Exception as exception:
            print("Error while running async job: "
                          f"{self.task_func}\nException: {exception}")

            error = exception
            _ex_type, _ex_value, trace = sys.exc_info()
            traceback.print_tb(trace)
            traceback_info = '\n'.join(traceback.format_tb(trace))

            print([str(exception), traceback_info])
        self.source_id = GLib.idle_add(self.callback, result, error)
        return self.source_id
