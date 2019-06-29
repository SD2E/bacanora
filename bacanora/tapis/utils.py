"""
Helper functions for working with Agave and Reactors APIs

```python
from tapis import *
```
"""
from __future__ import print_function

import re
import os
import time

import logging
logger = logging.getLogger(__name__)

from agavepy.agave import Agave
from attrdict import AttrDict

MAX_ELAPSED = 300
MAX_RETRIES = 5
FILES_HTTP_LINK_TYPES = ('media', 'download')
FILES_COMPATIBLE_APIS = ('files', 'jobs')
PWD = os.getcwd()

# TODO: Support nonces
# TODO: Support sending URL parameters
# TODO: Support binary FIFO?

# Normally, one can just inspect her API client to get these values
# but because Abaco creates ephemeral API clients using impersonation
# it's not always perfectly possible. These functions consult the
# local Abaco runtime context before trying heroically to pull the
# values out of the API client itself. This should preserve our ability
# to debug locally while still being able to access these three essential
# values from within Abaco functions.

__all__ = ['process_agave_httperror']


def get_api_server(ag):
    '''Get current API server URI'''
    if os.environ.get('_abaco_api_server'):
        return os.environ.get('_abaco_api_server')
    elif ag.token is not None:
        try:
            return ag.token.api_server
        except Exception as e:
            logger.error("ag.token was None: {}".format(e))
            pass
        return None
    else:
        logger.info("Used hard-coded value for API server")
        return None


def get_api_token(ag):
    '''Get API access_token'''
    if os.environ.get('_abaco_access_token'):
        return os.environ.get('_abaco_access_token')
    elif ag.token is not None:
        try:
            return ag.token.token_info.get('access_token')
        except Exception as e:
            logger.error("ag.token was None: {}".format(e))
            pass
        return None
    else:
        logger.error("Failed to retriev API access_token")
        return ""


def get_api_username(ag):
    '''Get current API username'''
    if os.environ.get('_abaco_username'):
        return os.environ.get('_abaco_username')
    elif ag is not None:
        try:
            return ag.username
        except Exception as e:
            logger.error("ag was None: {}".format(e))
        return None
    else:
        logger.error("No username could be determined")
        return None


def process_agave_httperror(http_error_object):

    h = http_error_object
    # extract HTTP response code
    code = -1
    try:
        code = h.response.status_code
        assert isinstance(code, int)
    except Exception:
        # we have no idea what the hell happened
        code = 418

    # extract HTTP reason
    reason = 'UNKNOWN ERROR'
    try:
        reason = h.response.reason
    except Exception:
        pass

    # Extract textual response elements
    #
    # agave and abaco will give json responses if the
    # underlying service is at all capable of doing so
    # so try to extract fields from it if we can.
    #
    # otherwise, return the actual text of the response
    # in error message
    err_msg = 'Unexpected encountered by the web service'
    status_msg = 'error'
    version_msg = 'unknown'
    try:
        j = h.response.json()
        if 'message' in j:
            err_msg = j['message']
        if 'status' in j:
            status_msg = j['status']
        if 'version' in j:
            version_msg = j['version']
    except Exception:
        err_msg = h.response.text

    httperror = 'HTTPError - {} {}; message: {}; status: {}; version: {}; response.content: {}'
    return httperror.format(code, reason, err_msg, status_msg, version_msg,
                            h.response.content)
