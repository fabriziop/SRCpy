
SRCpy, Segnale RAI Codificato (RAI Codified Signal)
===================================================

Encoder and decoder for the SRC time signal, Segnale RAI Codificato (RAI
Codified Signal), implemented in python language. This signal was broadcasted
in Italy to disseminate the national standard time. The SRC was developed
to be a signal suitable for broadcast through audio channels like radio/TV
by INRIM, Istituto Nazionale di Ricerca Metrologica, the italian NMI
(National Metrological Institute) that is in charge of the realization
of the national standard time (UTC-IT). The name RAI comes from one of
the major italian broadcaster.

This SRC implementation is focused to the offline encoding and decoding of the
signal. The coded signal is rendered as linear PCM audio that may be
stored to file (.wav) and decoded or played from file. The time to binary
encoding/decoding and the binary to audio encoding/decoding are in separate
single functions, with a simple API for extension to other applications.

Currently, this SRC implementation hasn't been tested on any hardware.

This SRC implementation is **not** endorsed by INRIM.


Signal structure
================

The SRC signal is structured to be broadcast once a minute as an audio signal,
so, it does not carry the seconds information and it is referred to the start
of the next minute.
For historical reasons the SRC signal was added to an existing simple
synchronization signal formed by 6 bursts of sinusoids at 1 kHz. Each burst
lasts 0.1 s and starts at the second start. The first burst is at second 54,
the following 4 bursts start respectively at seconds 55, 56, 57, 58. The last
burst start at second zero. This last burst is also the marker for the start
of the next minute to which the SRC signal refers.
::

                             SRC signal structure
                             ====================

     SRC binary code                    reference signal
   0s as 2.0kHz x 30ms                    1kHz x 100ms
   1s as 2.5kHz x 30ms 
        __________       ______________________________________________
       /          \     /       /       /      |       \               \
         Sg1   Sg2
       ||||||| ||||    ||      ||      ||      ||    ->||<-- 100 ms    ||
    ---|||||||-||||----||------||------||------||------||--------------||---
       ||||||| ||||    ||      ||      ||      ||      ||              ||

    ___|_______|_______|_______|_______|_______|_______|_______|_______|____
       52      53      54      55      56      57      58      59      00
    seconds of minute

The SRC binary code is divided in two segments: a first segment starting at
minute second 52, carrying 32 bits of time data and a second segment starting
at minute second 53, carrying 16 bits of time data.
The binary code is rendered as an audio signal by FSK modulation with a
30ms @ 2.0kHz symbol for each zero bit and with a 30ms @ 2.5kHz symbol for
each one bit.
::

                          SRC binary code, segment #1
               (example encoded time: Sat Apr  3 15:17:02 2021)
               ================================================

             bits 0-15 odd parity ____  bits 17-30 odd parity ______
            is DST flag (1->yes)  ___ \  day of week (mon.=1) ___   \
                                     \ \                         \   \
       |-id|----hour---|----minute---|-|-|--month--|-month day-|-----|-|
  BCD  |   |2 1        |4 2 1        | | |1        |2 1        |     | |
  units|   |0 0 8 4 2 1|0 0 0 8 4 2 1| | |0 8 4 2 1|0 0 8 4 2 1|4 2 1| |

  code |0 1|0 1 0 1 0 1|0 0 1 0 1 1 1|1|0|0 0 1 0 0|0 0 0 0 1 1|1 1 0|0|
    ___|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|____
  bit   0   2   4   6   8   10  12  14  16  18  20  22  24  26  28  30 
  _____|_________________________________________________________________|____
       52        seconds of minute                                       53

The first SRC segment carries the time information about hour, minute, month,
day of month, day of week and daylight saving in progress. The first 16 bits
and the following 15 bits are protected by two independent odd parity bits.
::

                          SRC binary code, segment #2
               (example encoded time: Sat Apr  3 15:17:02 2021)
               ================================================

            leap second alert ___
       days to DST change ___    \      ___ bits 0-14 odd parity 
                             \    \    /
       |-id|year (2 digits)|-----|---|-|
  BCD  |   |8 4 2 1        |     |   | |
  units|   |0 0 0 0 8 4 2 1|4 2 1|   | |

  code |1 0|0 0 1 0 0 0 0 1|1 1 1|0 0|1|
    ___|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|___
  bit   0   2   4   6   8   10  12  14  
  _____|_________________________________________________________________|____
       53        seconds of minute                                       54

  Note 1: days to DST change, code 111 -> no change within next 7 days,
          110 -> DST change within next 6 days, etc.
  Note 2: leap second alert, code 00 -> no leap second within current month,
          10 -> 1 delay second at month end,
          11 -> 1 avance second at month end. 

The second SRC segment carries the time information about the last two digits
of the year, the number of days before the next daylight saving change, if
less than 7, and the leap second alert information. This last information
is not yet implemented.


Requirements
============

To run the code, **Python 3.5 or later** must
already be installed.  The latest release is recommended.  Python is
available from http://www.python.org/.



Installation
============

1. Open a shell.

2. Get root privileges and install the package. Command::

    pip install srcpy


Code Repository
===============

There is also a code repository at `https://github.com/fabriziop/srcpy`_ .

.. _https://github.com/fabriziop/srcpy: https://github.com/fabriziop/srcpy


Examples
========

time_to_src
-----------

This example encodes a given time or the current computer local time into a
SRC signal as a wav file with linear PCM and int16 values. It print also the
time to be encoded and the SRC binary code segment #1 and #2 in both hexadecimal
and binary format. To generate the wav file *src.wav* for time
"Sat Apr  3 15:17:02 2021" run this example with the following command and
the following printed output
::

    $ time_to_src.py "Sat Apr  3 15:17:02 2021" src.wav
    signal segment #1: 552f103c hex 01010101001011110001000000111100 bin
    signal segment #2: 8879 hex 1000100001111001 bin

If the time is omitted from the command, the system time is used. Supposing
the system time to be "Sat Apr  3 15:17:02 2021" command and output are as
follows
::

    $ time_to_src.py src.wav
    encoded time: Sat Apr  3 15:17:02 2021
    signal segment #1: 552f103c hex 01010101001011110001000000111100 bin
    signal segment #2: 8879 hex 1000100001111001 bin


src_to_time
-----------

This example decodes a SRC signal from a wav file with a linear PCM int16
into a time.localtime structure. It print also the decoded time and the SRC
binary code segment #1 and #2 demodulated from the SRC audio signal.
To decode the wav file *src.wav* run this example with the following command
and the following printed outputs
::

    $ src_to_time.py src.wav
    signal segment #1: 552f103c hex 01010101001011110001000000111100 bin
    signal segment #2: 8879 hex 1000100001111001 bin
    decoded time: Sat Apr  3 15:17:00 2021


play_wav
--------

This is a simple utility to play a wav file on a computer. To play the wav
file *src.wav* run the command
::

    $ play_wav.py src.wav


API
===

srcpy.time_to_bin_code(time)
----------------------------

    Encode a RAI codified time signal (SRC) from a given time to a SRC
    binary code.

      **time**: tuple, the time tuple to be encoded with the following format
      (YY,MM,DD,HH,MM,WDAY,YDAY,ISDST), the time.localtime() format.

    Return pattern **segment1, segment2**

      **segment1**: integer, first segment of SRC binary coding (32bits).

      **segment2**: integer, second segment of SRC binary coding (16bits).


srcpy.bin_code_to_audio(bin_code,sampling_rate,data_type,amplitude)
-------------------------------------------------------------------

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


srcpy.audio_to_bin_code(audio,sampling_rate)
--------------------------------------------

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


srcpy.bin_code_to_time(bin_code)
--------------------------------

    Decode a RAI codified time signal (SRC) from binary code to time
    data structure.

      **bin_code**: tuple *(int seg1,int seg2)*, *seg1* SRC binary code
      segment 1 (32 bits), *seg2* SRC binary code segment 2 (16 bits).

    Return pattern **error_code,time**

      **error_code**: int, SUCCESS no error, ERR_SEG1_PARITY1 error on
      first code segment parity #1, ERR_SEG1_PARITY2 error on first
      code segment parity #2, ERR_SEG2_PARITY error on segment #2
      parity.

      **time**: tuple, the time data with the following format
      (YY,MM,DD,HH,MM,WDAY,YDAY,ISDST), the time.localtime() format.


Contributing
============

Send wishes, comments, patches, etc. to mxgbot_a_t_gmail.com .


Copyright
=========

SRCpy is authored by Fabrizio Pollastri <mxgbot_a_t_gmail.com>, year 2021, under the GNU Lesser General Public License version 3.

.. ==== END ====
