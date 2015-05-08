
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
- ``ERRBIT_APP_ID`` - your errbit app id (see URL when visiting the app).
- ``ERRBIT_API_KEY`` - your errbit API key.
- ``ERRBIT_PACKAGE`` - the setuptools name of your package.
- ``ERRBIT_ENVIRONMENT`` - the name of the environment you are running, such as
  ``staging`` or ``production``.
- ``ERRBIT_HTTP_CLIENT`` - Switch the http client implementation. Switching the
  implementation can solve different problems when communicating from private
  networks with HTTP proxies. Current implementations are: ``requests``, ``urllib``,
  ``urllib2``.
- ``ERRBIT_IGNORE`` - path to ignore file (default: ~/.errbit/errbit_ignore.json)

Ignore file
-----------

The thrown exception will be ignored and not passed to errbit if its message matches one of the regex in ``exception_msg``.

.. code:: json

    {
        "exception_msg": [
            "^AttributeError\\b",
            "regex2"
        ]
    }


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

For testing the connection you can call the view ``errbit-make-error`` as ``Manager``.

Report JavaScript errors in Plone
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In order to report JavaScript errors, install the Generic Setup profile
``profile-errbit.ploneintegration:default``, which registers the necessary
JavaScript resources.

For JavaScript reporting the ``ERRBIT_APP_ID`` environment variable needs to be set.

Test the configuration: if ``http://localhost:8080/Plone/errbit-plone.js`` is empty
not all enviornment variables are configured.


Development / tests
===================

Install the package and run the tests using buildout:

.. code:: sh

    git clone git@github.com:4teamwork/errbit-python.git
    cd errbit-python
    ln -s test-plone-4.3.x.cfg buildout.cfg
    python2.7 bootstrap.py
    bin/buildout
    bin/test


Links
-----

- Github: https://github.com/4teamwork/errbit-python
- Issues: https://github.com/4teamwork/errbit-python/issues
- Pypi: http://pypi.python.org/pypi/errbit-python
- Continuous integration: https://jenkins.4teamwork.ch/search?q=errbit-python


Copyright
---------

This package is copyright by `4teamwork <http://www.4teamwork.ch/>`_.

``errbit-python`` is licensed under GNU General Public License, version 2.
