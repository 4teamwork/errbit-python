import os
from setuptools import setup, find_packages


version = '1.4.0'


tests_require = [
    'ftw.testbrowser',
    'ftw.testing',
    'mocker',
    'plone.app.testing',
    'pyquery',
    'unittest2',
    'zope.component',
    'Plone',
    ]


setup(name='errbit',
      version=version,
      description='An errbit client for python',

      long_description=open('README.rst').read() + '\n' + \
          open(os.path.join('docs', 'HISTORY.txt')).read(),

      classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],

      keywords='errbit client python',
      author='4teamwork AG',
      author_email='mailto:info@4teamwork.ch',
      url='https://github.com/4teamwork/errbit-python',

      license='GPL2',
      packages=find_packages(exclude=['ez_setup']),
      include_package_data=True,
      zip_safe=False,

      install_requires=[
        'decorator',
        'requests',
        'setuptools',
        'xmlbuilder',
        ],

      tests_require=tests_require,
      extras_require=dict(tests=tests_require),

      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
