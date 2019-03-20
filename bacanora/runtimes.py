from os import environ
from . import logger as loggermodule

logger = loggermodule.get_logger(__name__)

__all__ = ['ABACO', 'JUPYTER', 'HPC', 'LOCALHOST', 'ALL', 'detect']

ABACO = 'abaco'
JUPYTER = 'jupyter'
HPC = 'hpc'
LOCALHOST = 'localhost'

ALL = (ABACO, JUPYTER, HPC, LOCALHOST)
DEFAULT_RUNTIME = ABACO

DEFINITIONS = {ABACO: 'Code is running inside an Abaco Reactor',
               JUPYTER: 'Code is running inside a Dockerized Jupyter notebook',
               HPC: 'Code is running natively on a TACC HPC system',
               LOCALHOST: 'Code is running locally'}

VARIABLES = {ABACO: 'REACTORS_VERSION',
            JUPYTER: 'JUPYTERHUB_USER',
            HPC: 'TACC_DOMAIN',
            LOCALHOST: 'DEADBEEF'}

class BacanoraRuntime(str):
    """Name of a BacanoraRuntime"""
    def __new__(cls, value):
        value = str(value).lower()
        setattr(cls, 'description', DEFINITIONS.get(value))
        if value not in list(DEFINITIONS.keys()):
            raise ValueError('"{}" is not a valid {}'.format(value, cls.__name__))
        return str.__new__(cls, value)

def detect():
    for runtime, variable in VARIABLES.items():
        if variable in environ:
            logger.debug('runtime: {}'.format(runtime))
            return BacanoraRuntime(runtime)
    logger.debug('runtime: {}'.format(DEFAULT_RUNTIME))
    return BacanoraRuntime(DEFAULT_RUNTIME)
