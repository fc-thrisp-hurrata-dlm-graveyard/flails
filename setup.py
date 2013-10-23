"""
Flails
------------

Flask application factory.

Flails provides some basics for generating a flask application from a specific
configuration & file structure


Links
`````
* `documentation <http://packages.python.org/>`_
* `development version
  <http://github.com/thrisp/flails>`_

"""
from setuptools import setup

setup(
    name='Flask-Flails',
    version='0',
    url='https://github.com/thrisp/flails',
    license='MIT',
    author='thrisp/hurrata',
    author_email='blueblank@gmail.com',
    description='Flask application factory',
    long_description=__doc__,
    packages=['flask_flails'],
    zip_safe=False,
    platforms='any',
    install_requires=[
        'Flask>=0.9',
        'Flask-Classy>=0.5.2',
        'Flask-Assets>=0.8'
    ],
    test_suite='nose.collector',
    tests_require=[
        'nose',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
