"""Provides rationalized logging with tunable verbosity
"""
import os
import sys
import logging
from enum import Enum
from bacanora import settings

LOG_NAME = 'bancanora'


class LogFormatter(object):
    STANDARD = logging.Formatter('%(name)s.%(levelname)s: %(message)s')
    VERBOSE = logging.Formatter(
        ("%(levelname)s in %(filename)s:%(funcName)s "
         "at line %(lineno)d occured at %(asctime)s\n\n\t%(message)s\n\n"
         "Full Path: %(pathname)s\n\nProcess Name: %(processName)s"))


def get_logger(module_name=None, level=None, verbose=None):
    """Get a configured Python logger object

    Arguments:
        module_name (str, optional): Override the detected name of the host module
        level (str, optional): Override the system default logging level
        verbose (bool, optional): Turn on an expansive format that includes tracebacks and line numbers

    Returns:
        logging: A Python ``logging`` object configured to write to STDERR
    """
    if module_name is None:
        module_name = __name__
    if level is None:
        level = settings.LOG_LEVEL
    if verbose is None:
        verbose = settings.LOG_VERBOSE

    logger = logging.getLogger(module_name)
    logger.setLevel(logging.getLevelName(level))
    loghandler = logging.StreamHandler()
    if verbose is True:
        loghandler.setFormatter(LogFormatter.VERBOSE)
    else:
        loghandler.setFormatter(LogFormatter.STANDARD)
    if len(logger.handlers) <= 0:
        logger.addHandler(loghandler)
    return logger
