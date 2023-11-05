# -*- coding: UTF-8 -*-
import os 
from setuptools import setup 

setup(
    name = 'my_app',
    version = '1.0',
    license = 'GNU General Public License v3',
    author = 'Tehmeer Ali Paryani',
    author_email = 'yout email.',
    description = 'Hello world application for Flask!',
    packages = ['my_app'],
    platforms = 'any',
    install_requires = [
        'flask',
    ],
    
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3',
        'Operating System :: OS Independent',
        'Programming Language :: Python Programming',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Programming Modules'
    ], 
    
)