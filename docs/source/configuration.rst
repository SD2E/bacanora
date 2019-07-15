Configuration
=============

Bacanora's behavior is controlled by environment variables:
    * ``BACANORA_STORAGE_SYSTEM`` - Default Agave storage system if not specified [``data-sd2e-community``]
    * ``BACANORA_LOG_LEVEL`` - Logging level for Bacanora's logging functions [``DEBUG``]
    * ``BACANORA_LOG_VERBOSE`` - Whether to emit *extremely* verbose log messages [``0``]
    * ``BACANORA_RETRY_MAX_DELAY`` - Maximum elapsed time before declaring a function has failed [``90``]
    * ``BACANORA_RETRY_RERAISE`` - Re-raise exceptions encountered during file operations [``0``]
    * ``BACANORA_FILES_BLOCK_SIZE`` - Size in bytes to retrieve in download operations [``4096``]
