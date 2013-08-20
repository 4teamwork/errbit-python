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
- ``ERRBIT_NOTIFIER_PACKAGE`` - the setuptools-name of your package. This by
  default be used as notifier name and the setuptools version of this package
  is used as notifier version.
- ``ERRBIT_NOTIFIER_NAME`` - sets the notifier name. Overrides ``ERRBIT_NOTIFIER_PACKAGE``.
- ``ERRBIT_NOTIFIER_VERSION`` - sets the notifier version. Overrides ``ERRBIT_NOTIFIER_PACKAGE``.
- ``ERRBIT_NOTIFIER_URL`` - sets the default notifier url.


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

        environment = {
            'environment-name': 'production',
            'app-version': '1.7',
            'project-root': '/app'}

        client.post(exc_info, request=request, environment=enviroment)



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
