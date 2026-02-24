''' -*- coding: utf8 -*-

 This file were created by Python Boilerplate. Use Python Boilerplate to start
 simple, usable and best-practices compliant Python projects.

 Learn more about it at: http://github.com/fabiommendes/python-boilerplate/
'''

import os

from setuptools import setup, find_packages

# Meta information

meta_dict = {}
for each in ['version', 'name', 'description', 'author', 'author_email']:
    with open(f'scripts/{each.upper()}', encoding="utf-8") as f:
        meta_dict[each] = f.read().strip()

dirname = os.path.dirname(__file__)

# Save version and author to __meta__.py
path = os.path.join(dirname, '__meta__.py')
data = f'''# Automatically created. Please do not edit.
__version__ = u'{meta_dict['version']}'
__author__ = u'{meta_dict['author']}'
'''
with open(path, 'wb') as F:
    F.write(data.encode())
with open('README.md', encoding="utf-8") as readme:
    long_description = readme.read()

with open('requirements.txt', encoding="utf-8") as reqs:
    requirements = reqs.readlines()

setup(
    # Basic info
    name=meta_dict['name'],
    version=meta_dict['version'],
    author=meta_dict['author'],
    author_email=meta_dict['author_email'],
    url='https://github.com/martyni/' + meta_dict['name'],
    description=meta_dict['description'],
    long_description=long_description,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries',
    ],

    # Packages and depencies
    package_dir={'': 'src'},
    packages=find_packages('src'),
    install_requires=requirements,
    extras_require={
        'dev': [
            'pytest',
            'autopep8',
            'pylint',
            'setuptools',
            'semantic-version'
        ],
    },

    # Data files
    package_data={
        'python_boilerplate': [
            'templates/*.*'
        ],
    },

    # Scripts
    entry_points={
        'console_scripts': [
            f"{meta_dict['name']}_web = webapp.app:main",
            f"{meta_dict['name']}   = myapp.app:main",
        ],
    },

    # Other configurations
    zip_safe=False,
    platforms='any',
)
