import re

module_file = open("delgado/__init__.py").read()
metadata = dict(re.findall("__([a-z]+)__\s*=\s*'([^']+)'", module_file))
long_description = open('README.rst').read()

from setuptools import setup, find_packages

setup(
    name = 'delgado',
    description = 'Command executor',
    packages = find_packages(),
    author = 'Alfredo Deza',
    author_email = 'alfredodeza [at] gmail.com',
    scripts = ['bin/delgado'],
    entry_points = dict(
        delgado_handlers = [
            'pytest = delgado.services:Pytest',
        ],
    ),
    install_requires = ['tambo'],
    version = metadata['version'],
    url = 'http://github.com/alfredodeza/delgado',
    license = "MIT",
    zip_safe = False,
    keywords = "commands, unix, socket, execute, terminal",
    long_description = long_description,
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Utilities',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
    ]
)
