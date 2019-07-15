Bacanora
========

Implements accelerated, failure-resilient versions of Agave files operations,
as well as analogues of several key Python `os.path` and `shutils` functions.
Acceleration is implemented via special IO optimizations available to machines
in TACC's data-enabled compute environment, while resliency comes from a
robust fail/retry system.

The ``bacanora.files`` module includes functions for file upload / download
(``put``, ``get``), status checks (``exists``, ``isfile``, ``isdir``,
``getsize``, ``mtime``), and management (``mkidr``, ``copy``,
``rename``, ``move``, ``delete``). There are also helper functions for
working with Tapis (``agave://``) URLs and TACC S3 (``s3://``) URLs

Usage Example
-------------

.. code-block:: pycon

   >>> from agavepy.agave import Agave
   >>> ag = Agave.restore()
   >>> import bacanora
   >>> bacanora.files.exists('/sample/tacc-cloud', agave=ag)
   True
    >>> bacanora.files.exists('/sample/tacc-cloud', system_id='data-projects-fake', agave=ag)
   False
   >>> bacanora.files.get('/sample/tacc-cloud/dawnofman.jpg', local_filename='ape.jpg', agave=ag)
   'ape.jpg'
   >>> bacanora.files.get('/sample/tacc-cloud/dawnofman.jpg', system_id='data-tacc-work-tacobot', agave=ag)
   'dawnofman.jpg'
   >>> bacanora.files.isdir('/sample/tacc-cloud', agave=ag)
   True
   >>> bacanora.files.isfile('/sample/tacc-cloud', agave=ag)
   False
   >>> bacanora.files.exists('/sample/tacc-cloud-fake', agave=ag)
   False

