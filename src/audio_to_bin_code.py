#!/usr/bin/env python3
# .+
# .context    : SRCpy, RAI coded signal (SRC)
# .title      : SRC decoding from linear PCM audio to time data
# .kind	      : python source
# .author     : Fabrizio Pollastri
# .site	      : Torino - Italy
# .creation   :	29-Mar-2021
# .copyright  :	(c) 2021 Fabrizio Pollastri
# .license    : GNU Lesser General Public License
# .-


from srcpy.common import *

import scipy.signal as ss

import matplotlib.pyplot as pl


#### functions

def audio_to_bin_code(audio,sampling_rate):
    """
    Demodulate a RAI codified time signal (SRC) from audio linear
    PCM binary to SRC binary code. The signal is demodulated using
    the envelope of symbols correlation. 

      **audio**: numpy array, SRC signal in audio format as linear PCM
      signal. 

      **sampling_rate**: integer, encode the signal at this sample per
      second rate.

    Return pattern **(int seg1,int seg2)**

      **seg1**: SRC binary code segment 1 (32 bits).

      **seg2**: SRC binary code segment 2 (16 bits).
    """

    ## symbols to look for: bursts of sinusoidal cycles

    # zero and one symbol coding (sc0 and sc1): 30ms @2kHz and 30ms @2.5kHz
    amplitude = audio.max()
    sc0 = sin_burst(SYMBOL_ZERO_FREQ,amplitude,SYMBOL_PERIOD,
        sampling_rate,type(audio[0]))
    sc1 = sin_burst(SYMBOL_ONE_FREQ,amplitude,SYMBOL_PERIOD,
        sampling_rate,type(audio[0]))

    ## demodulate codified time signal: FSK 0/1 30ms@2kHz/30ms@2.5kHz

    # envelope of 0/1 symbols correlation
    sc0_env =np.abs(ss.hilbert(ss.correlate(audio.astype(np.float),sc0)))
    sc1_env =np.abs(ss.hilbert(ss.correlate(audio.astype(np.float),sc1)))

    # find the start of first signal segment (first symbol middle time):
    # first envelop maxima of 0 symbol correlation.
    data_pitch = sampling_rate * SYMBOL_PERIOD
    sc0_env_threshold = sc0_env.max() / 2.,
    sc1_env_threshold = sc1_env.max() / 2.,
    first_symbol_pos = min(
      ss.find_peaks(sc0_env,height=sc0_env_threshold,distance=data_pitch)[0][0],
      ss.find_peaks(sc1_env,height=sc1_env_threshold,distance=data_pitch)[0][0])

    # extract data of first signal segment: sample correlation envelope
    # at data pitch (32 bits)
    segment1 = 0
    for i in range(0,32):
        segment1 <<= 1
        sample_pos = int(first_symbol_pos + i * data_pitch)
        if sc1_env[sample_pos] - sc0_env[sample_pos] > 0:
            segment1 |= 0x1

    # extract data of second signal segment: sample correlation envelope
    # at data pitch (16 bits)
    segment2 = 0
    first_symbol_pos = int(sample_pos+sampling_rate*(SEG1_SEG2_GAP + SYMBOL_PERIOD))
    for i in range(0,16):
        segment2 <<= 1
        sample_pos = int(first_symbol_pos + i * data_pitch)
        if sc1_env[sample_pos] - sc0_env[sample_pos] > 0:
            segment2 |= 0x1 

    return segment1,segment2

#### END
