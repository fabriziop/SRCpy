#!/usr/bin/env python3
# .+
# .context    : iSRCpy, RAI coded signal (SRC)
# .title      : package setup
# .kind       : python script
# .author     : Fabrizio Pollastri <mxgbot@gmail.com>
# .site       : Revello - Italy
# .creation   : 30-Mar-2021
# .copyright  : (c) 2021 Fabrizio Pollastri
# .license    : GNU Lesser General Public License
# .-

import os
from setuptools import setup

setup(
    name = 'srcpy',
    packages = ['srcpy'],
    package_dir = {'srcpy':'src'},
    include_package_data = True,
    install_requires = ['dateutils','numpy','scipy'],
    scripts = ['examples/time_to_src.py','examples/src_to_time.py',
        'examples/play_wav.py'],
    version_command = ('git describe --tags'))
#    version_command = ('git describe --tags','pep440-git-dev'))

# define global variables
__script__ = os.path.basename(__file__)
__author__ = 'Fabrizio Pollastri <mxgbot@gmail.com>'

#### END
