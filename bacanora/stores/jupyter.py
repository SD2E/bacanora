"""Definitions for JupyterHub and Notebooks environments
"""

import os

__all__ = ['JUPYTER_URL_BASE', 'JUPYTER_HUB_BASE', 'JUPYTER_HPC_BASE']

JUPYTER_URL_BASE = '/user/{User}/tree'
JUPYTER_HUB_BASE = '/home/jupyter'
JUPYTER_HPC_BASE = os.environ.get('HOME', JUPYTER_HUB_BASE)
