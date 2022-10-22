class GradienceError(Exception):
    """Base class for exceptions in this module."""

    pass


class GradienceMonetError(GradienceError):
    """Exception raised for errors in the Monet module."""

    pass


class GradienceMonetUnsupportedBackgroundError(GradienceMonetError):
    """Exception raised for errors in the monet module with an unsupported background type."""

    pass
