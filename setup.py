# -*- coding: utf-8 -*-
"""
This module contains the tool of pointerstop.recipe.hostout
"""
import os
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = '1.0'

long_description = (
    read('README.txt')
    + '\n' +
    'Detailed Documentation\n'
    '**********************\n'
    + '\n' +
    read('pointerstop', 'recipe', 'hostout', 'README.txt')
    + '\n' +
    'Contributors\n' 
    '************\n'
    + '\n' +
    read('CONTRIBUTORS.txt')
    + '\n' +
    'Change history\n'
    '**************\n'
    + '\n' + 
    read('CHANGES.txt')
    + '\n' +
   'Download\n'
    '********\n'
    )
entry_point = 'pointerstop.recipe.hostout:Recipe'
entry_points = {"zc.buildout": ["default = %s" % entry_point]}

tests_require=['zope.testing', 'zc.buildout']

setup(name='pointerstop.recipe.hostout',
      version=version,
      description="Build supervisor control statements for each instance running on same host as this hostout",
      long_description=long_description,
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        'Framework :: Buildout',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        ],
      keywords='http://pointerstop.ca/',
      author='Derek Broughton',
      author_email='auspex@pointerstop.ca',
      url='http://pointerstop.ca/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['pointerstop', 'pointerstop.recipe'],
      include_package_data=True,
      zip_safe=False,
      install_requires=['setuptools',
                        'zc.buildout'
                        # -*- Extra requirements: -*-
                        ],
      tests_require=tests_require,
      extras_require=dict(tests=tests_require),
      test_suite = 'pointerstop.recipe.hostout.tests.test_docs.test_suite',
      entry_points=entry_points,
      )
