"""The ``tapis`` submodule wraps common ``files`` operations (and select
other APIs) in a common access pattern that provides resilient, optimized
performance (where possible), and alignment with the behavior of file & path
management functions in Python's ``os`` module.
"""
from . import entity
from . import pems
from .agave import AgaveNonceOnly
from .exceptions import *
from .operations import *
from .utils import get_api_server, get_api_token, get_api_username
# from .reactors import send_message, await_actor_execution
from .uri import to_agave_uri, from_tacc_s3_uri, from_agave_uri

# @retry(
#     retry=retry_if_exception_type(AgaveError),
#     reraise=RETRY_RERAISE,
#     stop=stop_after_delay(RETRY_MAX_DELAY),
#     wait=wait_exponential(multiplier=2, max=64))
