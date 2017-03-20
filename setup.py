#! python
#
import io
import os
import re
import sys

from setuptools import setup, find_packages


if sys.version_info < (3, 4):
    msg = "Sorry, Python >= 3.4 is required, but found: {}"
    sys.exit(msg.format(sys.version_info))


proj_name = 'pyradiri'
mydir = os.path.dirname(__file__)


# Version-trick to have version-info in a single place,
# taken from: http://stackoverflow.com/questions/2058802/how-can-i-get-the-version-defined-in-setup-py-setuptools-in-my-package
##
def read_project_version():
    fglobals = {}
    with io.open(os.path.join(
            mydir, 'pyradiri', '_version.py'), encoding='UTF-8') as fd:
        exec(fd.read(), fglobals)  # To read __version__
    return fglobals['__version__']


def read_text_lines(fname):
    with io.open(os.path.join(mydir, fname)) as fd:
        return fd.readlines()


def yield_rst_only_markup(lines):
    """
    :param file_inp:     a `filename` or ``sys.stdin``?
    :param file_out:     a `filename` or ``sys.stdout`?`

    """
    substs = [
        # Selected Sphinx-only Roles.
        #
        (r':abbr:`([^`]+)`', r'\1'),
        (r':ref:`([^`]+)`', r'ref: *\1*'),
        (r':term:`([^`]+)`', r'**\1**'),
        (r':dfn:`([^`]+)`', r'**\1**'),
        (r':(samp|guilabel|menuselection|doc|file):`([^`]+)`',
                                    r'``\2``'),

        # Sphinx-only roles:
        #        :foo:`bar`   --> foo(``bar``)
        #        :a:foo:`bar` XXX afoo(``bar``)
        #
        #(r'(:(\w+))?:(\w+):`([^`]*)`', r'\2\3(``\4``)'),
        #(r':(\w+):`([^`]*)`', r'\1(`\2`)'),
        # emphasis
        # literal
        # code
        # math
        # pep-reference
        # rfc-reference
        # strong
        # subscript, sub
        # superscript, sup
        # title-reference


        # Sphinx-only Directives.
        #
        (r'\.\. doctest', r'code-block'),
        (r'\.\. module', r'code-block'),
        (r'\.\. plot::', r'.. '),
        (r'\.\. seealso', r'info'),
        (r'\.\. glossary', r'rubric'),
        (r'\.\. figure::', r'.. '),
        (r'\.\. image::', r'.. '),

        (r'\.\. dispatcher', r'code-block'),

        # Other
        #
        (r'\|version\|', r'x.x.x'),
        (r'\|today\|', r'x.x.x'),
        (r'\.\. include:: AUTHORS', r'see: AUTHORS'),
    ]

    regex_subs = [(re.compile(regex, re.IGNORECASE), sub)
                  for (regex, sub) in substs]

    def clean_line(line):
        try:
            for (regex, sub) in regex_subs:
                line = regex.sub(sub, line)
        except Exception as ex:
            print("ERROR: %s, (line(%s)" % (regex, sub))
            raise ex

        return line

    for line in lines:
        yield clean_line(line)


proj_ver = read_project_version()
readme_lines = read_text_lines('README.rst')
description = readme_lines[1]
long_desc = ''.join(yield_rst_only_markup(readme_lines))
download_url = 'https://github.com/JRCSTU/pyradiri/releases/tag/v%s' % proj_ver

setup(
    name=proj_name,
    version=proj_ver,
    description="A CRUD application for hierarchical folder metadata based on a JSON-schema & YAML.",
    long_description=long_desc,
    download_url=download_url,
    keywords="metadata, folders, directories, filesystem, database".split(),
    url='https://github.com/JRCSTU/pyradiri/',
    license='EUPL 1.1+',
    author='Kostis Anagnostopoulos',
    author_email='ankostis@gmail.com',
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: Implementation :: CPython",
        "Development Status :: 3 - Alpha",
        'Natural Language :: English',
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        'Environment :: Console',
        'License :: OSI Approved :: European Union Public Licence 1.1 (EUPL 1.1)',
        'Natural Language :: English',
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Operating System :: Unix",
        "Operating System :: OS Independent",
        "Topic :: Database",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Text Processing :: Indexing",
        "Topic :: Utilities",
    ],
    setup_requires=[
        # PEP426-field actually not used by `pip`, hence
        # included also in /requirements/developmnet.pip.
        'setuptools',
        'setuptools-git>=0.3',  # Example given like that in PY docs.
        'wheel',
    ],
    # dev_requires=[
    #     # PEP426-field actually not used by `pip`, hence
    #     # included in /requirements/developmnet.pip.
    #     'sphinx',
    # ],
    install_requires=[
        'rainbow_logging_handler',
        'ruamel.yaml',
        'jsonschema',
        'strict-rfc3339',  # for date-tie schema parsing
        'boltons',
        'toolz',
    ],
    packages=find_packages(exclude=[
        'tests', 'tests.*',
        'doc', 'doc.*',
    ]),
    package_data={
        'pyradiri': [
            '*.yaml',
            '*.ipynb',
        ]
    },
    include_package_data=True,
    zip_safe=True,
    test_suite='nose.collector',
    tests_require=['nose>=1.0', 'ddt'],
    entry_points={
        'console_scripts': [
            '%(p)s = %(p)s.__main__:main' % {'p': proj_name},
        ],
    },
    options={
        'bdist_wheel': {
            'universal': True,
        },
    },
    platforms=['any'],
)
