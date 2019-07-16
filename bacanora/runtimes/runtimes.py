from os import environ
from .. import logger as loggermodule

logger = loggermodule.get_logger(__name__)

__all__ = [
    'ABACO', 'JUPYTER', 'HPC_JUPYTER', 'HPC', 'LOCALHOST', 'ALL', 'detect',
    'UnknownRuntime', 'RuntimeNotDetected', 'BacanoraRuntime',
    'DEFAULT_RUNTIME'
]

ABACO = 'abaco'
JUPYTER = 'jupyter'
HPC_JUPYTER = 'hpc_jupyter'
HPC = 'hpc'
LOCALHOST = 'localhost'
AUTO = 'auto'

ALL = (ABACO, JUPYTER, HPC_JUPYTER, HPC, LOCALHOST, AUTO)
DEFAULT_RUNTIME = ABACO

DEFINITIONS = {
    ABACO: 'Code is running inside an Abaco Reactor',
    JUPYTER: 'Code is running inside a Dockerized Jupyter notebook',
    HPC_JUPYTER: 'Code is running inside a HPC Singularity container',
    HPC: 'Code is running natively on a TACC HPC system',
    LOCALHOST: 'Code is running locally',
}

# TODO - Expand list of variables and/or runtimes supported
VARIABLES = {
    ABACO: ['REACTORS_VERSION', '_abaco_actor_dbid'],
    JUPYTER: ['JUPYTERHUB_USER', 'JUPYTERHUB_API_TOKEN'],
    HPC_JUPYTER: ['TACC_SINGULARITY_DIR', 'JUPYTER_WORK', 'TACC_DOMAIN'],
    HPC: ['TACC_DOMAIN', 'SLURM_CLUSTER_NAME', 'TACC_SYSTEM'],
    LOCALHOST: ['LOCALONLY']
}


class UnknownRuntime(ValueError):
    """Not a known runtime name
    """
    pass


class RuntimeNotDetected(Exception):
    """Not possible to automatically detect the environment
    that the code in running in
    """
    pass


class BacanoraRuntime(str):
    """Extended string name for a Bacanora runtime"""

    def __new__(cls, value):
        value = str(value).lower()
        setattr(cls, 'description', DEFINITIONS.get(value))
        if value not in list(DEFINITIONS.keys()):
            raise UnknownRuntime('"{}" is not a valid {}'.format(
                value, cls.__name__))
        return str.__new__(cls, value)


def detect(override=None, permissive=True):
    """Detect which runtime the calling code is running in
    using environment fingerprinting
    """
    if override is not None:
        return BacanoraRuntime(override)
    for runtime, variables in VARIABLES.items():
        vars_match = 0
        for varname in variables:
            if varname in environ:
                logger.debug('Detected {}'.format(varname))
                vars_match = vars_match + 1
        if vars_match == len(variables):
            logger.debug('Runtime is "{}"'.format(runtime))
            return BacanoraRuntime(runtime)
    if permissive:
        logger.debug('runtime: {}'.format(DEFAULT_RUNTIME))
        return BacanoraRuntime(DEFAULT_RUNTIME)
    else:
        raise RuntimeNotDetected(
            'Unable to determine current runtime environment')
