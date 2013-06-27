"""

Flails
------------

"Flask is really not at all like Ruby-on-Rails but sometimes you need
an app factory and some configuration conventions"

Flails provides some basics for generating a flask application
from a specific configuration


Links
`````
* `documentation <http://packages.python.org/>`_
* `development version
  <http://>`_

"""
from flask_flails import __version__
from setuptools import setup

requires = ['Flask>=0.9',
            'Flask-Classy>=0.5.2',
            'Flask-Assets>=0.8']

setup(
    name='Flask-Flails',
    version=__version__,
    url='http://',
    license='MIT',
    author='thrisp/hurrata',
    author_email='blueblank@gmail.com',
    description='Flask application factory',
    long_description=__doc__,
    packages=['flask_flails'],
    test_suite="test",
    zip_safe=False,
    platforms='any',
    install_requires=requires,
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
