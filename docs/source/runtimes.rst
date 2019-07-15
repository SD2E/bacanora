Runtimes
========

The predominant use case for Bacanora is to provide optimized file operations
on servers operated by TACC, known as "data-enabled compute hosts", where the
backing storage for various Tapis storageSystems is available as a mounted
directories as a supplement to the API-native access methods. This is
implemented in a variety of ways, depending on the kind of computing host and
the intended use case for the storageSystem. In any case, avoiding direct
usage of the backend paths is a best practice, so Bacanora was designed to
enable operations using only the Tapis-relative paths.

Bacanora can detect and operate in the following runtime environments:
    * Abaco: TACC's functions-as-a-service platform
    * HPC: TACC login nodes or batch computing serevrs
    * Jupyter: TACC-hosted Jupyter Notebooks or the Jupyter Terminal

It can handle operations on the following types of storage system:
    * Community: Tapis tenant-wide shared, managed storage (``data-sd2e-community``)
    * Work: A user's TACC WORK directory (``data-tacc-work-maryj``)
    * Share: Collaborative file-share resources (``data-sd2e-projects.genome-sequencing``)
    * Project: Subproject resources (``data-projects-safegenes``)
