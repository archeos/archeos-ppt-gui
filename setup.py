#!/usr/bin/env python
from distutils.core import setup

setup(name='PPT-GUI',
 version='0.1',
 description='A simple GUI for Python Photogrammetry Toolbox',
 author='Alessendro Bezzi, Luca Bezzi',
 author_email='alessandro.bezzi@arcteam.com, luca.bezzi@arteam.com',
 url='http://www.archeos.eu',
 license='GPL2',
 packages = ['gui'],
 package_data = {'gui' : ['assets/icons/info_icon.png', 
	 	'assets/icons/python_icon.png'
	 	],
	},
 scripts=['ppt-gui.py'],
 data_files=[
	 ('doc/ppt-gui', ['README.md'])
	 ],
 requires=['ppt (>= 0.1)','pyQt4 (>= 4.9.3)'],
 )
