#!/usr/bin/python3
# .+
# .context    : SRCpy, RAI coded signal (SRC)
# .title      : SRC encoding from time data to SRC binary code
# .kind	      : python source
# .author     : Fabrizio Pollastri
# .site	      : Torino - Italy
# .creation   :	29-Jan-2017
# .copyright  :	(c) 2017 Fabrizio Pollastri
# .license    : GNU Lesser General Public License
# .-


from srcpy.common import *


#### functions

def time_to_bin_code(time):
    """
    Encode a RAI codified time signal (SRC) from a given time to a SRC
    binary code.

      **time**: tuple, the time tuple to be encoded with the following format
      (YY,MM,DD,HH,MM,WDAY,YDAY,ISDST), the time.localtime() format.

    Return pattern **segment1, segment2**

      **segment1**: integer, first segment of SRC binary coding (32bits).

      **segment2**: integer, second segment of SRC binary coding (16bits).
    """

    ## segment #1 bit coding

    # bit 1-0: segment one id
    seg1 = SEG1ID

    # bits 7-2: hours,
    # bcd weights for bits 7-2 20,10,8,4,2,1
    hours = time[HOURS]
    seg1 <<= 2
    seg1 |= hours // 10
    seg1 <<= 4
    seg1 |= hours % 10
 
    # bits 14-8: minutes,
    # bcd weights for bits 14-8 40,20,10,8,4,2,1
    minutes = time[MINUTES]
    seg1 <<= 3
    seg1 |= minutes // 10
    seg1 <<= 4
    seg1 |= minutes % 10

    # bit 15: time zone 1 = ST, 0 = DST
    seg1 <<= 1 
    if time[ISDST]:
        seg1 |= 0x1
 
    # bit 16: even parity for id, hours, minutes, dst
    seg1 <<= 1 
    if parity(seg1 & 0x1fffe):
        seg1 |= 0x1

    # bits 21-17: month of year,
    # bcd weights for bits 21-17 10,8,4,2,1 (1: Jan)
    month = time[MONTH]
    seg1 <<= 1
    seg1 |= month // 10
    seg1 <<= 4
    seg1 |= month % 10

    # bits 27-22: day of month,
    # bcd weights for bits 27-22 20,10,8,4,2,1
    month_day = time[MONTH_DAY]
    seg1 <<= 2 
    seg1 |= month_day // 10
    seg1 <<= 4
    seg1 |= month_day % 10

    # bits 30-28: day of week,
    # bcd weights for secs 30-28 4,2,1 (1: Monday; 7: Sunday)
    seg1 <<= 3
    seg1 |= time[WEEK_DAY] + 1

    # bit 31: even parity for month, day of month, day of week
    seg1 <<= 1
    if parity(seg1 & 0x7ffe):
        seg1 |= 0x1


    ## segment #2 bit coding

    # bit 1-0: segment two id
    seg2 = SEG2ID
 
    # bits 9-2: year of the century,
    # bcd weights for bits 9-2 80,40,20,10,8,4,2,1
    year = time[YEAR] % 100
    seg2 <<= 4
    seg2 |= year // 10
    seg2 <<= 4
    seg2 |= year % 10

    # bits 12-10: DST alert,
    # 111 : no alert
    # 110 : change after 6 day
    # ...
    # 001 : change next day
    # 000 : change @02:00 or @03:00
    seg2 <<=3
    days = days_to_next_dst_change()
    if days >= 7:
        seg2 |= 0x7
    else:
        seg2 |= days

    # bits 14-13: leap second alert,
    # 00 : no alert
    # 10 : subtract one second at the end of month
    # 11 : add one second at the end of month
    # NOT YET IMPLEMENTED
    seg2 <<= 2

    # bits 15: even parity for id, year, DST alert and leap second alert
    seg2 <<= 1
    if parity(seg2 & 0xfffe):
        seg2 |= 0x1

    return seg1,seg2

#### END
