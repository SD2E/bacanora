"""Support for mapping TACC S3 buckets onto select Tapis storageSystems
"""
import os
import re
from .. import stores
from .. import settings
from ..utils import normalize, normpath
from .corral import BASEPATHS
from .system import S3NotSupported

from ..logger import get_logger
logger = get_logger(__name__)

PROTO = re.compile("s3://([a-zA-Z0-9-_.]+)/?(.*)?$")
BUCKET_MAPPINGS = [('uploads', 'data-sd2e-community', '/')]

__all__ = [
    's3_to_tapis', 'from_s3_uri', 'to_s3_uri', 'system_props_from_bucket'
]


def s3_to_tapis(bucket_name, bucket_path):
    """Map a TACC S3 bucket & path to its corresponding Tapis system_id and path
    Args:
        bucket_name (str): A TACC S3 bucket
        bucket_path (str): Absolute path within the bucket

    Raises:
        S3NotSupported: The resolved storageSystem does not yet support S3 uploads

    Returns:
        tuple: (storageSystem.id, absolute_path)
    """

    # (bucket_name, bucket_path) = from_s3_uri(s3_uri)
    (system_id, system_root, system_type,
     system_shortname) = system_props_from_bucket(bucket_name)

    # Validate that the storageSystem can support S3
    if BASEPATHS.get(system_type, None) is None:
        raise S3NotSupported(
            '{} is a {}-type system which does not support S3 uploads'.format(
                system_id, system_type))

    # Return Tapis resources
    logger.debug('Tapis from {} and {}'.format(system_id, bucket_path))
    return (system_id, os.path.join(system_root, normalize(bucket_path)))


def system_props_from_bucket(bucket_name):
    """Fetch Tapis storageSystem properties by S3 bucket name
    """
    system_id = None
    for bucket, sys_id, sys_root in BUCKET_MAPPINGS:
        if bucket_name == bucket:
            logger.debug('mapping: {} => {}{}'.format(bucket_name, sys_id,
                                                      sys_root))
            system_id = sys_id
            system_root = sys_root
    if system_id is None:
        system_id = bucket_name
        system_root = '/'
    system_type, system_shortname = stores.system_type_and_name(system_id)
    return (system_id, system_root, system_type, system_shortname)


def from_s3_uri(s3_uri, verify=False):
    """Resolve TACC S3 uri into its bucket and path

    Args:
        s3_uri (str): A URI of form s3://tacc-bucket-name/path/to/file.txt
        verify (bool, optional): Validate that the resource exists

    Returns:
        tuple: (bucket_name, bucket_abs_path)

    Raises:
        ValueError: URI is not recognized as a TACC S3 resource
    """
    resources = PROTO.search(s3_uri)
    if not resources:
        raise ValueError('Not a TACC S3 URI: {}'.format(s3_uri))

    bucket_name = resources.group(1).lower()
    logger.debug('bucket_name: {}'.format(bucket_name))
    bucket_path = normpath(resources.group(2))
    if bucket_path in ('', '.'):
        bucket_path = '/'

    return (bucket_name, bucket_path)


def to_s3_uri(bucket_name, bucket_path, verify=False):
    """Resolve TACC S3 uri into its bucket and path

    Args:
        bucket_name (str): A TACC S3 bucket
        bucket_path (str): Absolute path within the bucket
        verify (bool, optional): Validate that the resource exists

    Returns:
        string: A URI of form s3://tacc-bucket-name/path/to/file.txt

    Raises:
        ValueError: Bucket name or path is invalid
    """
    s3_uri = 's3://{}{}'.format(bucket_name.lower(), normpath(bucket_path))
    if verify:
        logger.warning('The "exists" option is not yet suppported')
    return s3_uri
