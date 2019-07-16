"""Constants for the Corral resource.
"""

from .. import stores
from .. import settings

__all__ = [
    'BASEPATHS', 'HPC_BASE', 'ABACO_BASE', 'JUPYTER_BASE', 'S3_PROJECT_BASE'
]

CORRAL_CONTAINER_BASE = '/corral'
CORRAL_NATIVE_BASE = '/corral-repl/projects/{}'.format(
    settings.TACC_PROJECT_NAME)

S3_PROJECT_BASE = '/s3/ingest'

HPC_BASE = CORRAL_NATIVE_BASE
ABACO_BASE = CORRAL_CONTAINER_BASE
JUPYTER_BASE = CORRAL_CONTAINER_BASE

BASEPATHS = {
    stores.COMMUNITY_TYPE: {
        'src': '{}/uploads'.format(S3_PROJECT_BASE),
        'dest': '/uploads'
    },
    stores.SHARE_TYPE: None,
    stores.PROJECT_TYPE: {
        'src': '{0}/{1}'.format(S3_PROJECT_BASE, '{}'),
        'dest': ''
    }
}
