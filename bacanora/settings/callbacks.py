import os
from .helpers import (fix_assets_path, array_from_string, parse_boolean,
                      int_or_none, set_from_string)

__all__ = []

# Callback targets
# TODO - These are in anticipation of webhook support on given actions
# Email target
DEFAULT_CALLBACK_EMAIL = os.environ.get('BACANORA_CALLBACK_EMAIL',
                                        'bounces@devnull.com')
# POST target
DEFAULT_CALLBACK_URI = os.environ.get('BACANORA_CALLBACK_URI',
                                      'https://devnull.com/')
