"""For creating and validating Hashids
"""
from hashids import Hashids
from uuid import uuid3, uuid5, NAMESPACE_DNS
from . import settings

__all__ = ["generate", "validate"]

HASHIDS_SALT = settings.HASHIDS_SALT


def dns_namespace():
    return uuid3(NAMESPACE_DNS, 'tacc.cloud')


def generate(*args):
    """Generate a unique Hashid for one or more passed values

    Arguments:
        args: One or more values to serialize into an identifier. Passed
        values must support str(<value>).

    Returns:
        str: A Hashid that is distinct to contents of *args
    """
    values = [str(v) for v in args]
    hashids = Hashids(salt=HASHIDS_SALT)
    serialized_text_value = '.'.join(values)
    uuid_from_vals = uuid5(dns_namespace(), serialized_text_value)
    return hashids.encode(uuid_from_vals.int)


def validate(text_string, permissive=False):
    """Validate whether a string is a hashid

    Arguments:
        text_string (str): the value to validate
        permissive (bool, optional): whether to return false or raise Exception on failure

    Raises:
        ValueError: The passed value was not a Hashid and permissive was `False`

    Returns:
        bool: Whether the passed value is a Hashid

    Warning:
        This is better for opt-in classification than formal valdiation as there are several edge cases than can render a false negative.
    """
    result = is_hashid(text_string)
    if result is True:
        return result
    else:
        if permissive is False:
            raise ValueError(
                '{} not a valid hashid for this namespace'.format(text_string))
        else:
            return False


def is_hashid(identifier):
    hashids = Hashids(salt=HASHIDS_SALT)
    dec = hashids.decode(identifier)
    if len(dec) > 0:
        return True
    else:
        return False
