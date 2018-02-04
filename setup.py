# This Python file uses the following encoding: utf-8

"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/thegalactic/py-galactic
"""

# To use a consistent encoding
from codecs import open
from os import path

# Always prefer setuptools over distutils
from setuptools import setup

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
try:
    import pypandoc

    long_description = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError):
    with open(path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()

try:
    from sphinx.setup_command import BuildDoc
    cmdclass = {'build_sphinx': BuildDoc}
except ImportError:
    cmdclass = {}

name = 'py-galactic'
version = '0.0'
release = '0.0.2'
author = 'The Galactic Organization'
author_email='contact@thegalactic.org'

setup(
    name=name,

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html

    version=release,
    cmdclass=cmdclass,
    # these are optional and override conf.py settings
    command_options={
        'build_sphinx': {
            'project': ('setup.py', name),
            'version': ('setup.py', version),
            'release': ('setup.py', release),
        }
    },

    # The project's description
    description='A package for Formal Concept Analysis',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/thegalactic/py-galactic',

    # The project's download page
    download_url='https://github.com/thegalactic/py-galactic/archive/master.zip',

    # Author details
    author=author,
    author_email=author_email,

    # Maintainer details
    maintainer=author,
    maintainer_email=author_email,

    # Choose your license
    license='BSD-3-Clause',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   1 - Planning
        #   2 - Pre-Alpha
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        #   6 - Mature
        #   7 - Inactive
        'Development Status :: 2 - Pre-Alpha',

        # Specify the OS
        'Operating System :: OS Independent',

        # Indicate who your project is intended for
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.6',

        # Natural language used
        'Natural Language :: English',
    ],

    # What does your project relate to?
    keywords='formal concept analysis',

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=[
        'bitstring>=3.1'
    ],

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage3'],
    },

    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    package_data={},

    setup_requires=[
        'pytest-runner',
        'pypandoc>=1.4',
        'sphinx>=1.6',
        'sphinx_rtd_theme>=0.2.4'
    ],
    tests_require=['pytest', 'coverage'],

    packages=[
        'galactic',
        'galactic.context',
        'galactic.context.memory'
    ],
)
