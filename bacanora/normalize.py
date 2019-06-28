import os
import re


def normalize(filepath):
    # Prefixes are terminated with '/' to indicate they are directories. In
    # order to avoid double-slashes, which causes os.path.join() to fail,
    # strip out leading slash
    fp = re.sub('^(/)+', '', filepath)
    return fp


def normpath(filepath):
    fp = re.sub('^(/)+', '/', filepath)
    return os.path.normpath(fp)
