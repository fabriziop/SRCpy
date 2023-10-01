#!/usr/bin/env python3
# .+
# .context    : SRCpy, RAI coded signal (SRC)
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
    long_description = 'Encoder/decoder for the SRC time signal',
    long_description_content_type = 'text/x-rst',
    url = 'https://github.com/fabriziop/SRCpy',
    packages = ['srcpy'],
    package_dir = {'srcpy':'src'},
    include_package_data = True,
    install_requires = ['python-dateutil','numpy','scipy'],
    scripts = ['examples/time_to_src.py','examples/src_to_time.py',
        'examples/play_wav.py'],
    version = "0.1.5")

# define global variables
__script__ = os.path.basename(__file__)
__author__ = 'Fabrizio Pollastri <mxgbot@gmail.com>'

#### END
