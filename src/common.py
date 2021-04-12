#!/usr/bin/python3
# .+
# .context    : SRCpy, RAI coded signal (SRC)
# .title      : common definitions and functions
# .kind	      : python source
# .author     : Fabrizio Pollastri
# .site	      : Torino - Italy
# .creation   :	27-Mar-2021
# .copyright  :	(c) 2021 Fabrizio Pollastri
# .license    : GNU Lesser General Public License
# .-


from datetime import datetime as dt
from dateutil import tz
import numpy as np	# array support
import math as mt	# circular functions
import time as tm


#### constants

# time tuple offsets
YEAR,MONTH,MONTH_DAY,HOURS,MINUTES,SECONDS,WEEK_DAY,YEAR_DAY,ISDST = \
    range(9)

# identifiers
SEG1ID = 0x1
SEG2ID = 0x2

# signal timings (s, Hz)
SYMBOL_PERIOD = 0.03
SYMBOL_ZERO_FREQ = 2000
SYMBOL_ONE_FREQ = 2500
SIG_ELAPSE_TIME = 8.1
SEG1_START = 0
SEG2_START = 1
SEG1_SEG2_GAP = 0.04
REF_PULSE_PERIOD = 0.1
REF_PULSE_FREQ = 1000
REF_PULSE_STARTS = (2,3,4,5,6,8)

SEG1_SYMBOL_NUM = 32
SEG2_SYMBOL_NUM = 16

#### error codes

SUCCESS = 0
ERR_SEG1_PARITY1 = -1
ERR_SEG1_PARITY2 = -2
ERR_SEG2_PARITY = -3


#### functions

def sin_burst(frequency,amplitude,duration,sampling_rate,data_type):
    """
    Return a burst of sinusoidal wave with given and constant amplitude,
    frequency, duration, sampling rate and data type.

      **frequency**: float or int, burst frequency.

      **amplitude**: float or int, half peak to peak signal amplitude.

      **duration**: float or int, burst lasting in seconds.

      **sampling_rate**: integer, signal sample per second.

      **data_type**: string, data type of the encoded signal, one of
          'float32','int32','int16','uint8'.


    Return pattern **burst**

      **burst**: numpy array of type specified by *data_type*
      argument, a sinusoidal burst signal with given frequency, duration,
      amplitude, sampling rate and data type.
    """
    
    sample_num = int(duration * sampling_rate)
    burst = np.zeros(sample_num,data_type)
    pi2 = mt.pi * 2
    sin_cycle_sample_num = float(sampling_rate) / frequency
    for i in range(sample_num):
        burst[i] = amplitude * mt.sin(i / sin_cycle_sample_num * pi2)

    return burst


def parity(value):
    """
    Return 1 for even bit number, 0 for odd bit number.
    """
    ones = 0
    while value:
        value &= value - 1
        ones += 1
    return ~ones & 1


def days_to_next_dst_change():
    z = tz.gettz()
    now = dt.now()
    next_dst_change = z._trans_list_utc[z._find_last_transition(now) + 1]
    next_dst_change_midnight = next_dst_change - next_dst_change % 86400
    secs_to_next_dst_change = next_dst_change_midnight - tm.time()
    if secs_to_next_dst_change > 0:
        return secs_to_next_dst_change // 86400 + 1
    else:
        return 0


#### END
