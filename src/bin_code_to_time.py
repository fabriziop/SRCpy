#!/usr/bin/env python3
# .+
# .context    : SRCpy, RAI coded signal (SRC)
# .title      : SRC decoding from SRC binary code to time
# .kind	      : python source
# .author     : Fabrizio Pollastri
# .site	      : Torino - Italy
# .creation   :	30-Mar-2021
# .copyright  :	(c) 2021 Fabrizio Pollastri
# .license    : GNU Lesser General Public License
# .-


from srcpy.common import *

import time as tm


#### functions

def bin_code_to_time(bin_code):
    """
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
    """

    ## segment #1 bit decoding
 
    seg1 = bin_code[0]

    # parity check
    if parity(seg1 & 0xffff8000):
        return ERR_SEG1_PARITY1,None
    if parity(seg1 & 0x7fff):
        return ERR_SEG1_PARITY2,None

    # bits 30-28: day of week,
    # bcd weights for secs 30-28 4,2,1 (1: Monday; 7: Sunday)
    seg1 >>= 1
    week_day = (seg1 & 0x7) - 1
    seg1 >>= 3

    # bits 27-22: day of month,
    # bcd weights for bits 27-22 20,10,8,4,2,1
    month_day = seg1 & 0xf
    seg1 >>= 4
    month_day += (seg1 & 0x3) * 10
    seg1 >>= 2

    # bits 21-17: month of year,
    # bcd weights for bits 21-17 10,8,4,2,1 (1: Jan)
    month = seg1 & 0xf
    seg1 >>= 4
    month += (seg1 & 0x1) * 10
    seg1 >>= 1
        
    # bit 16: even parity for id, hours, minutes, dst
    # year of the century
    # skip it for now
    seg1 >>= 1

    # bit 15: time zone 1 = ST, 0 = DST
    isdst = seg1 & 0x1 
    seg1 >>= 1

    # bits 14-8: minutes,
    # bcd weights for bits 14-8 40,20,10,8,4,2,1
    minute = seg1 & 0xf
    seg1 >>= 4
    minute += (seg1 & 0x7) * 10
    seg1 >>= 3

    # bits 7-2: hours,
    # bcd weights for bits 7-2 20,10,8,4,2,1
    hour = seg1 & 0xf
    seg1 >>= 4
    hour += (seg1 & 0x3) * 10
    seg1 >>= 2

    # bit 0-1: segment one id
    # skip it for now


    ## segment #2 bit decoding

    seg2 = bin_code[1]

    # parity check
    if parity(seg1 & 0xffff):
        return ERR_SEG2_PARITY,None
    seg2 >>= 1 
 
    # bits 14-13: leap second alert,
    # 00 : no alert
    # 10 : subtract one second at the end of month
    # 11 : add one second at the end of month
    # NOT YET IMPLEMENTED
    # skip ti for now
    seg2 >>= 2

    # bits 12-10: DST alert,
    # 111 : no alert
    # 110 : change after 6 day
    # ...
    # 001 : change next day
    # 000 : change @02:00 or @03:00
    # NOT YET IMPLEMENTED
    # skip ti for now
    seg2 >>= 3
  
    # bits 9-2: year of the century,
    # bcd weights for bits 9-2 80,40,20,10,8,4,2,1
    year = seg2 & 0xf
    seg2 >>= 4
    year += (seg2 & 0xf) * 10
    seg2 >>= 4

    # bit 1-0: segment two id
    # skip it for now
    seg2 >>= 2

    return SUCCESS,tm.struct_time([2000 + year,month,month_day,hour,
        minute,0,week_day,0,isdst])

#### END
