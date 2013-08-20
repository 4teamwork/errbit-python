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

- ``ERRBIT_API_KEY`` - your errbit API key.
- ``ERRBIT_NOTIFIER_PACKAGE`` - the setuptools-name of your package. This by
  default be used as notifier name and the setuptools version of this package
  is used as notifier version.
- ``ERRBIT_NOTIFIER_NAME`` - sets the notifier name. Overrides ``ERRBIT_NOTIFIER_PACKAGE``.
- ``ERRBIT_NOTIFIER_VERSION`` - sets the notifier version. Overrides ``ERRBIT_NOTIFIER_PACKAGE``.
- ``ERRBIT_NOTIFIER_URL`` - sets the default notifier url.



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
