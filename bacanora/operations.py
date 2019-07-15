"""Import commands that are handled by the ``processor`` mechanism
"""
from .download import (get)
from .manage import (mkdir, delete, copy, move, rename)
from .stat import (exists, isfile, isdir)
from .upload import (put)
from .pems import (grant)
from .walk import (walk, listdir)
# from .version import (version)
