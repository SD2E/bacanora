"""Supports path-mapping on various runtimes for each functional kind of Tapis
storageSystem
"""
import inspect
import json
import os
import re
from functools import lru_cache
from .exceptions import ManagedStoreError, UnknownStorageSystem
from ..extensible import ExtensibleAttrDict
from ..utils import normalize, normpath
from .. import settings
from .. import hashable
from .. import runtimes
from .jupyter import (JUPYTER_BASE)
from .types import (COMMUNITY_TYPE, PROJECT_TYPE, PUBLIC_TYPE, SHARE_TYPE,
                    WORK_TYPE, SYSTEM_TYPES)

__all__ = [
    'COMMUNITY_TYPE', 'PROJECT_TYPE', 'PUBLIC_TYPE', 'SHARE_TYPE', 'WORK_TYPE',
    'SYSTEM_TYPES', 'JUPYTER_BASE', 'StorageSystem', 'abspath',
    'system_type_and_name'
]

REGEXES = {
    COMMUNITY_TYPE: re.compile('data-(sd2e-community)'),
    PUBLIC_TYPE: re.compile('data-sd2e-projects-(users)'),
    SHARE_TYPE: re.compile('data-sd2e-projects.([-.a-zA-Z0-9]{4,})'),
    PROJECT_TYPE: re.compile('data-projects-([-.a-zA-Z0-9]{4,})'),
    WORK_TYPE: re.compile('data-tacc-work-([a-zA-Z0-9]{3,8})')
}


class StorageSystem(str):
    """Abstract representation of an Tapis API storage system
    """

    def __new__(cls, value, agave=None):
        value = str(value).lower()
        # if value not in dict(cls.MEMBERS):
        #     raise ValueError('"{}" is not a known {}'.format(value, cls.__name__))
        return str.__new__(cls, value)

    def __init__(self, name, local=True, agave=None):
        super().__init__()
        self.set_type_and_name(permissive=False)
        assert agave is not None, 'StorageSystem requires a valid API client'
        setattr(self, 'client', agave)
        setattr(self, '_cache', self.get_system_record(permissive=False))

    def set_type_and_name(self, permissive=False):
        """Uses regular expressions to find type and short name for system
        """
        try:
            tn = system_type_and_name(self, permissive=permissive)
            setattr(self, '_type', tn[0])
            setattr(self, '_short_name', tn[1])
        except Exception:
            if permissive is False:
                raise ManagedStoreError(
                    'Unable to determine type/short name for {}'.format(self))

    @hashable.picklecache.mcache(lru_cache(maxsize=256))
    def get_system_record(self, permissive=False):
        modfile = inspect.getfile(self.__class__)
        storefile = os.path.join(os.path.dirname(modfile), 'systems.json')
        # load in mappings.json
        # array of system defs, mirroring response from agave.systems.list()
        contents = json.load(open(storefile, 'r'))
        for system in contents:
            # SHOULD THIS BE system.get('id') == name
            if system.get('id') == self:
                return ExtensibleAttrDict(system)
        try:
            sys = self.client.systems.get(systemId=self)
            return ExtensibleAttrDict(sys)
        except Exception as exc:
            raise UnknownStorageSystem(
                'Unable to fetch StorageSystem {} [{}]'.format(self, str(exc)))

    @property
    def system_id(self):
        return self._cache.id

    @property
    def name(self):
        return self._cache.name

    @property
    def description(self):
        return self._cache.description

    @property
    def owner(self):
        return self._cache.owner

    @property
    def page_size(self):
        return 50

    @property
    def ssh_host(self):
        if self._cache.storage['protocol'] == 'SFTP':
            return self._cache.storage['host'] + ':' + str(
                self._cache.storage['port'])
        else:
            raise ManagedStoreError(
                '{} is not an SSH-based POSIX system'.format(self.name))

    @property
    def type(self):
        return self._type

    @property
    def short_name(self):
        return self._short_name

    @property
    def home_dir(self):
        return self._cache.storage['homeDir']

    @property
    def root_dir(self):
        return self._cache.storage['rootDir']

    def agave_dir(self, path):
        agave_base = self.root_dir + self.home_dir
        agave_dir = path.replace(agave_base, '/')
        agave_dir = re.sub('^/+', '/', agave_dir)
        return agave_dir

    @property
    def work_dir(self):
        return self.root_dir

    @property
    def hpc_dir(self):
        return self.work_dir

    @property
    def abaco_dir(self):
        return self.work_dir

    def _jupyter_user_base(self):
        return '/user/' + self.short_name + '/tree'

    @property
    def jupyter_dir(self):
        if self.type == COMMUNITY_TYPE:
            return os.path.join(JUPYTER_BASE, self._short_name)
        elif self.type == WORK_TYPE:
            return self._jupyter_user_base() + '/tacc-work'
        elif self.type == SHARE_TYPE:
            return os.path.join(JUPYTER_BASE, 'sd2e-projects', self.short_name)
        elif self.type == PROJECT_TYPE:
            return os.path.join(JUPYTER_BASE, 'sd2e-partners', self.short_name)
        elif self.type == PUBLIC_TYPE:
            # We do not allow any exposure of the Agave public system assets
            # via Jupyter, esp. because we use it to store application assets
            raise ManagedStoreError('{} is not available via Jupyter'.format(
                self.system_id))
        else:
            raise ManagedStoreError('Failed to resolve Jupyter path')

    @property
    def localhost_dir(self):
        return os.environ.get('BACANORA_LOCALHOST_ROOT_DIR',
                              os.path.join(os.getcwd(), 'temp'))

    def agave_canonical_uri(self, path):
        """Return a agave-canonical URI for a path on the StorageSystem
        """
        uri = 'agave://{}/{}'.format(self.system_id, normalize(path))
        return uri

    def agave_http_uri(self, path, downloadable=False):
        """Return a HTTPS URI for a path on the StorageSystem
        """
        if downloadable:
            context = 'download'
        else:
            context = 'media'
        uri = '{}files/v2/{}/system/{}/{}'.format(settings.TACC_API_SERVER,
                                                  context, self.system_id,
                                                  normalize(path))
        return uri

    def jupyterhub_http_uri(self, path, username='{User}'):
        """Return a JupyterHub-canonical URI for a path on the StorageSystem
        """
        path = self.runtime_dir(runtimes.JUPYTER, path)
        uri = '{}{}'.format(settings.TACC_JUPYTER_SERVER, path)
        return uri

    def sftp_uri(self, path, username='<username>'):
        """Returns an SFTP uri for HPC systems

        Note: Implements RFC-3986 (expired) encoding for SFTP URIs
        """
        path = self.runtime_dir(runtimes.HPC, path)
        uri = 'sftp://{}@{}/{}'.format(username, self.ssh_host,
                                       normalize(path))
        return uri

    @classmethod
    def jupyter_path_uri(self, path):
        return settings.TACC_JUPYTER_SERVER + path

    def runtime_dir(self, runtime, path):
        if runtime == runtimes.ABACO:
            runtime_path = self.abaco_dir
        elif runtime == runtimes.HPC:
            runtime_path = self.hpc_dir
        elif runtime == runtimes.JUPYTER:
            runtime_path = self.jupyter_dir
        else:
            runtime_path = self.localhost_dir
        path = normalize(path)
        return os.path.join(runtime_path, path)


def abspath(self, filepath, storage_system=None, validate=False, agave=None):
    """Resolve absolute path on host filesystem for an Agave path"""
    normalized_path = normalize(filepath)
    if os.environ.get('STORAGE_SYSTEM_PREFIX_OVERRIDE', None) is not None:
        root_dir = os.environ.get('STORAGE_SYSTEM_PREFIX_OVERRIDE')
    else:
        root_dir = StorageSystem(storage_system, agave=agave).root_dir
    return os.path.join(root_dir, normalized_path)


def system_type_and_name(system_id, permissive=False):
    system_type = None
    system_short_name = None
    for t, r in REGEXES.items():
        rs = r.match(system_id)
        if rs:
            system_type = t
            system_short_name = rs.group(1)
            return (system_type, system_short_name)
    if permissive is False:
        raise ManagedStoreError(
            'Unable to determine type/short name for {}'.format(system_id))
