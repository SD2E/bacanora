from . import __version__


def version(*args, **kwargs):
    return 'bacanora.' + str(__version__)
