import pluggy

hookspec = pluggy.HookspecMarker("gradience")


class PrinterHooks:
    @hookspec
    def validate(msg):
        "validate hook"
        pass

    @hookspec
    def apply(msg):
        "apply hook"
        pass

    @hookspec
    def save(msg):
        "save hook"
        pass
