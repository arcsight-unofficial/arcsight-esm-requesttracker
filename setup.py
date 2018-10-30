#!/usr/bin/env python
from distutils.core import setup

setup(name='arcsightrequesttracker',
      version='1.0',
      description='ArcSight Request Tracker Integration',
      author='Marius Iversen',
      author_email='marius@chasenet.org',
      url='https://github.com/P1llus/arcsight-esm-requesttracker',
      packages=['arcsightrequesttracker.arcsightesm', 'arcsightrequesttracker.requesttracker'],
)
