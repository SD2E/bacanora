import os.path

# As per https://packaging.python.org/guides/single-sourcing-package-version/
# Example 3, warehouse
# https://github.com/pypa/warehouse/blob/64ca42e42d5613c8339b3ec5e1cb7765c6b23083/warehouse/__about__.py

__all__ = [
    "__title__",
    "__summary__",
    "__uri__",
    "__version__",
    "__commit__",
    "__author__",
    "__email__",
    "__license__",
    "__copyright__",
]

try:
    base_dir = os.path.dirname(os.path.abspath(__file__))
except NameError:
    base_dir = None

__title__ = 'bacanora'
__summary__ = 'Accelerated, resilient Tapis file operations'
__uri__ = ''
__version__ = '1.0.0-rc1'

if base_dir is not None and os.path.exists(os.path.join(base_dir, ".commit")):
    with open(os.path.join(base_dir, ".commit")) as fp:
        __commit__ = fp.read().strip()
else:
    __commit__ = None

__author__ = "Matthew Vaughn"
__email__ = "opensource@tacc.cloud"

__license__ = "BSD-3"
__copyright__ = "2019 %s" % __author__


def version(*args, **kwargs):
    return 'bacanora.' + str(__version__)
