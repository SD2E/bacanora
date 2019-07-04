from bacanora import __version__


def version(*args, **kwargs):
    return 'bacanora.direct.' + str(__version__)
