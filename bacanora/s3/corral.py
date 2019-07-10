"""Constants for TACC's Corral resource, which is the backing
store for TACC S3 services
"""

from .. import stores
from .. import settings

__all__ = [
    'BASEPATHS', 'HPC_BASE', 'ABACO_BASE', 'JUPYTER_BASE', 'S3_PROJECT_BASE'
]

CORRAL_CONTAINER_BASE = '/corral'
CORRAL_BASE = '/corral-repl/projects'

S3_PROJECT_BASE = '/{}/s3/ingest'.format(settings.TACC_PROJECT_NAME)

HPC_BASE = CORRAL_BASE
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
