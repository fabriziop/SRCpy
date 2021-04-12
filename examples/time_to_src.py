#!/usr/bin/python3
# .+
# .context    : SRCpy, RAI coded signal (SRC)
# .title      : SRC encoding to wav file
# .kind	      : python source
# .author     : Fabrizio Pollastri
# .site	      : Torino - Italy
# .creation   :	28-Mar-2021
# .copyright  :	(c) 2021 Fabrizio Pollastri
# .license    : GNU Lesser General Public License
# .usage
#
# Mode 1: encode system time.
#   ./time_to_src.py <output_wav_file_name>
#
# Mode 2: encode given time. Example time string "Sat Apr 10 01:17:03 2021".
#   ./time_to_src.py "<time_string>" <output_wav_file_name>
#
# .-

from srcpy.common import *
from srcpy import time_to_bin_code, bin_code_to_audio

import scipy.io.wavfile as wv
import sys


#### constants

FILE_NAME = 'src.wav'
DATA_RATE = 44100
DATA_TYPE = np.int16
AMPLITUDE = 10000


#### main

if len(sys.argv) < 3:
    # if it is specified only the output file, take time from system.
    now = tm.localtime()
    outfile = sys.argv[1]
    print('encoded time:',tm.asctime(now))
else:
    # if time is specified on command line, take it.
    now = tm.strptime(sys.argv[1])
    outfile = sys.argv[2]

bin_code = time_to_bin_code(now)
print(
    'signal segment #1: {:08x} hex {:032b} bin'.format(bin_code[0],bin_code[0]))
print(
    'signal segment #2: {:04x} hex {:016b} bin'.format(bin_code[1],bin_code[1]))
audio = bin_code_to_audio(bin_code,DATA_RATE,DATA_TYPE,AMPLITUDE)
wv.write(outfile,DATA_RATE,audio)

#### END
