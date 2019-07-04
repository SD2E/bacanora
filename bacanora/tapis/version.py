from bacanora import __version__


def version(*args, **kwargs):
    return 'bacanora.tapis.' + str(__version__)
