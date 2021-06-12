#!/usr/bin/python3
# .+
# .context    : SRCpy, RAI coded signal (SRC)
# .title      : decode a SRC signal from linear PCM audio to time
# .kind	      : python source
# .author     : Fabrizio Pollastri
# .site	      : Torino - Italy
# .creation   :	21-Mar-2021
# .copyright  :	(c) 2021 Fabrizio Pollastri
# .license    : GNU Lesser General Public License
# .usage
#    ./src_to_time.py <input_wav_file_name>
#
# .-

from srcpy.common import *
from srcpy import audio_to_bin_code, bin_code_to_time

import sys
import wave


# open a wav format file containing the SRC signal
fsrc = wave.open(sys.argv[1],"rb")

# read in SRC signal as linear PCM audio
audio = np.frombuffer(fsrc.readframes(-1),np.int16)

# demodulate SRC audio to SRC binary code
bin_code = audio_to_bin_code(audio,fsrc.getframerate())
print(
    'signal segment #1: {:08x} hex {:032b} bin'.format(bin_code[0],bin_code[0]))
print(
    'signal segment #2: {:04x} hex {:016b} bin'.format(bin_code[1],bin_code[1]))

# decode SRC binary code to time structure
err_code,time = bin_code_to_time(bin_code)
if err_code:
    print('error code:',err_code)
else:
    print('decoded time:',tm.asctime(time))

#### END
