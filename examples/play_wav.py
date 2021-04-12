#!/usr/bin/python3
# .+
# .context    : SRCpy, RAI coded signal (SRC)
# .title      : play a wav file
# .kind	      : python source
# .author     : Fabrizio Pollastri
# .site	      : Torino - Italy
# .creation   :	31-Mar-2021
# .copyright  :	(c) 2021 Fabrizio Pollastri
# .license    : GNU Lesser General Public License
# .usage
#
#   ./play_wav.py <wav_file_name_to_play>
#
# .-

import pyaudio as pa
import sys
import time as tm
import wave

#define stream chunk
chunk = 1024

#open a wav format file
f = wave.open(sys.argv[1],"rb")

#instantiate PyAudio
pya = pa.PyAudio()

#open stream
stream = pya.open(format = pya.get_format_from_width(f.getsampwidth()),
    channels = f.getnchannels(), rate = f.getframerate(), output = True)

#read data
data = f.readframes(chunk)

#play stream
while data:
    stream.write(data)
    data = f.readframes(chunk)
tm.sleep(0.1)

#stop stream
stream.stop_stream()
stream.close()

#close PyAudio
pya.terminate()

#### END
