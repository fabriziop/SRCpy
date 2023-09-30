#!/usr/bin/end python3
# .+
# .context    : SRCpy, RAI coded signal (SRC)
# .title      : SRC encoding from binary code to linear PCM audio
# .kind	      : python source
# .author     : Fabrizio Pollastri
# .site	      : Torino - Italy
# .creation   :	28-Mar-2021
# .copyright  :	(c) 2021 Fabrizio Pollastri
# .license    : GNU Lesser General Public License
# .-


from srcpy.common import *


#### functions

def bin_code_to_audio(bin_code,sampling_rate,data_type,amplitude):
    """
    Encode a RAI codified time signal (SRC) from binary code to audio
    linear PCM with a given sampling rate and data type.

      **bin_code**: two integer tuple, first element is SRC segment 1, the
      second is segment 2.

      **sampling_rate**: integer, encode the signal at this sample per second
      rate.

      **data_type**: string, data type of the encoded signal, one of
      'np.float32','np.int32','np.int16','np.uint8'.

      **amplitude**: same type of data_type, half peak to peak signal amplitude.

    Return pattern **audio**

      **audio**: numpy array of type specified by *data_type* argument, a
      time signal encoded into SRC audio format as linear PCM signal. 
    """


    ## sinusoidal bursts

    # reference pulse coding (rpc): 100ms @ 1kHz
    rpc = sin_burst(REF_PULSE_FREQ,amplitude,REF_PULSE_PERIOD,
        sampling_rate,data_type)

    # zero and one symbol coding (sc0 and sc1): 30ms @2kHz and 30ms @2.5kHz
    sc0 = sin_burst(SYMBOL_ZERO_FREQ,amplitude,SYMBOL_PERIOD,
        sampling_rate,data_type)
    sc1 = sin_burst(SYMBOL_ONE_FREQ,amplitude,SYMBOL_PERIOD,
        sampling_rate,data_type)

    # allocate PCM signal array
    audio = np.zeros(int(SIG_ELAPSE_TIME * sampling_rate),data_type)

    # insert segment one
    seg1 = bin_code[0]
    seg1_start = SEG1_START * sampling_rate
    symbol_end = seg1_start
    mask = 0x80000000
    for bit in range(SEG1_SYMBOL_NUM):
        symbol_start = symbol_end
        symbol_end += len(sc0)
        if seg1 & mask:
            audio[symbol_start:symbol_end] = sc1
        else:
            audio[symbol_start:symbol_end] = sc0
        mask >>= 1
 
    # insert segment two
    seg2 = bin_code[1]
    seg2_start = SEG2_START * sampling_rate
    symbol_end = seg2_start
    mask = 0x8000
    for bit in range(SEG2_SYMBOL_NUM):
        symbol_start = symbol_end
        symbol_end += len(sc0)
        if seg2 & mask:
            audio[symbol_start:symbol_end] = sc1
        else:
            audio[symbol_start:symbol_end] = sc0
        mask >>= 1
  
    # insert reference pulses
    for ref_pulse_start in REF_PULSE_STARTS:
        ref_pulse_start = ref_pulse_start * sampling_rate
        ref_pulse_end = ref_pulse_start + len(rpc)
        audio[ref_pulse_start:ref_pulse_end] = rpc

    return audio

#### END
