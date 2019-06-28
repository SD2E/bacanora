from os import environ
from .. import logger as loggermodule

logger = loggermodule.get_logger(__name__)

__all__ = [
    'ABACO', 'JUPYTER', 'HPC', 'LOCALHOST', 'ALL', 'detect', 'UnknownRuntime',
    'RuntimeNotDetected', 'BacanoraRuntime'
]

ABACO = 'abaco'
JUPYTER = 'jupyter'
HPC = 'hpc'
LOCALHOST = 'localhost'

ALL = (ABACO, JUPYTER, HPC, LOCALHOST)
DEFAULT_RUNTIME = LOCALHOST

DEFINITIONS = {
    ABACO: 'Code is running inside an Abaco Reactor',
    JUPYTER: 'Code is running inside a Dockerized Jupyter notebook',
    HPC: 'Code is running natively on a TACC HPC system',
    LOCALHOST: 'Code is running locally'
}

# TODO - Expand list of variables and/or runtimes supported
VARIABLES = {
    ABACO: ['REACTORS_VERSION'],
    JUPYTER: ['JUPYTERHUB_USER'],
    HPC: ['TACC_DOMAIN'],
    LOCALHOST: ['DEADBEEF']
}


class UnknownRuntime(ValueError):
    pass


class RuntimeNotDetected(Exception):
    pass


class BacanoraRuntime(str):
    """Name of a BacanoraRuntime"""

    def __new__(cls, value):
        value = str(value).lower()
        setattr(cls, 'description', DEFINITIONS.get(value))
        if value not in list(DEFINITIONS.keys()):
            raise UnknownRuntime('"{}" is not a valid {}'.format(
                value, cls.__name__))
        return str.__new__(cls, value)


def detect(permissive=True):
    for runtime, variables in VARIABLES.items():
        for varname in variables:
            if varname in environ:
                logger.debug('Detected {}'.format(varname))
                logger.debug('Runtime is "{}"'.format(runtime))
                return BacanoraRuntime(runtime)
    if permissive:
        logger.debug('runtime: {}'.format(DEFAULT_RUNTIME))
        return BacanoraRuntime(DEFAULT_RUNTIME)
    else:
        raise RuntimeNotDetected(
            'Unable to determine current runtime environment')
