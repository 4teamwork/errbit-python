===================
 errbit for python
===================

An `errbit <http://errbit.github.io/errbit/>`_ client for python.


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
