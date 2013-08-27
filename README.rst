
===================
 errbit for python
===================

An `errbit <http://errbit.github.io/errbit/>`_ client for python.


Installation
============

Add `errbit` to your package dependencies in `setup.py` or `requirements.txt`.


Configuration
=============

Configure errbit with environment variables:

- ``ERRBIT_URL`` - the post-url to your errbit installation.
- ``ERRBIT_API_KEY`` - your errbit API key.
- ``ERRBIT_PACKAGE`` - the setuptools name of your package.
- ``ERRBIT_ENVIRONMENT`` - the name of the environment you are running, such as
  ``staging`` or ``production``.


Usage
=====

The ``errbit`` package ships with the core notification implementation for errbit
and integrations for some frameworks.


Manually posting exceptions
---------------------------

Use the errbit client to post exceptions to an errbit installation:

.. code:: python

    from errbit.client import Client
    import sys

    client = Client()
    try:
        do_something()
    except:
        exc_info = sys.exc_info()

        request = {
            'url': 'http://my.app/app/folders/create',
            'component': 'folders',
            'action': 'create',
            'params': {
                'title': 'My Folder'},
            'session': {
                'cookie': 'session_id=123345'},
            'cgi-data': {
                'HTTP_X_FORWARDED_HOST': 'my.app'}}

        client.post(exc_info, request=request)


Plone
-----

Plone integration is automatically done with a logging handler,
nothing needs to be done for enabling it beside configuring the environment variables.


Development / tests
===================

Install the package and run the tests using buildout:

.. code:: shell

    git clone git@github.com:4teamwork/errbit-python.git
    cd errbit-python
    ln -s test-plone-4.3.x.cfg buildout.cfg
    python2.7 bootstrap.py
    bin/buildout
    bin/test


Links
-----

- Main github project repository: https://github.com/4teamwork/errbit-python
- Issue tracker: https://github.com/4teamwork/errbit-python/issues
- Package on pypi: http://pypi.python.org/pypi/errbit-python
- Continuous integration: https://jenkins.4teamwork.ch/search?q=errbit-python


Copyright
---------

This package is copyright by `4teamwork <http://www.4teamwork.ch/>`_.

``errbit-python`` is licensed under GNU General Public License, version 2.

.. image:: https://cruel-carlota.pagodabox.com/2b54f90882a606963f8e0581193f51bb
   :alt: githalytics.com
   :target: http://githalytics.com/4teamwork/errbit-python
