from ..preset import Preset
import pluggy

hookspec = pluggy.HookspecMarker("gradience")


@hookspec
def apply(preset: Preset):
    pass


@hookspec
def save(preset: Preset):
    pass


@hookspec
def validate(preset: Preset):
    pass


@hookspec
def enable():
    pass


@hookspec
def disable():
    pass


@hookspec
def check():
    pass


@hookspec
def settings(preset: Preset):
    pass
