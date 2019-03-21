Bacanora
========

Implements accelerated, failure-resilient versions of Agave files operations,
as well as analogues of key Python `os.path` and `shutils` functions.

Currently supported functions include:
    * ``upload``
    * ``download``
    * ``grant``
    * ``exists``
    * ``isdir``
    * ``isfile``
    * ``mkdir``
    * ``delete``

Configuration
-------------

Bacanora's behavior is controlled by environment variables:
    * ``BACANORA_STORAGE_SYSTEM`` - Default Agave storage system if not specified [``data-sd2e-community``]
    * ``BACANORA_LOG_LEVEL`` - Logging level for Bacanora's logging functions [``DEBUG``]
    * ``BACANORA_LOG_VERBOSE`` - Whether to emit *extremely* verbose log messages [``0``]
    * ``BACANORA_RETRY_MAX_DELAY`` - Maximum elapsed time before declaring a function has failed [``90``]
    * ``BACANORA_RETRY_RERAISE`` - Re-raise exceptions encountered during file operations [``0``]
    * ``BACANORA_FILES_BLOCK_SIZE`` - Size in bytes to retrieve in download operations [``4096``]

Usage Example
-------------

.. code-block:: pycon

   >>> import bacanora
   >>> from agavepy.agave import Agave
   >>> ag = Agave.restore()
   >>> bacanora.exists(ag, '/sample/tacc-cloud')
   True
   >>> bacanora.download(ag, ' /sample/tacc-cloud/bacanora/blebob.jpg', local_filename='billie.jpg')
   'billie.jpg'
   >>> bacanora.isdir(ag, '/sample/tacc-cloud')
   True
   >>> bacanora.isfile(ag, '/sample/tacc-cloud')
   False
   >>> bacanora.exists(ag, '/sample/tacc-cloud-fake')
   False
