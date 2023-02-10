import math

from sgp4.earth_gravity import wgs84
from sgp4.io import twoline2rv
from pymap3d.ecef import ecef2geodetic
from datetime import timedelta, datetime
import re, calendar

tle = "tle.txt"
aoslos = "AOSLOS.txt"  ##file with the next aos and los

with open(aoslos, "r") as f:
    x = f.readlines()
    for txt in x:
        if "AOS:" in txt:
            
            aostxt = txt[txt.find("AOS")+9:txt.find(" @ ")-2]
            aostxt = aostxt[:aostxt.rfind(" ")]
            aosdt = datetime.strptime(aostxt, "%b %d %H:%M:%S %Y")

            lostxt = txt[txt.find("LOS")+9:]
            lostxt = lostxt[:lostxt.find(" @ ")-2]
            lostxt = lostxt[:lostxt.rfind(" ")]

            losdt = datetime.strptime(lostxt, "%b %d %H:%M:%S %Y")


            aos_timestamp = int(re.search(r'AOS:.*?(\d+) @', txt).group(1))
            los_timestamp = int(re.search(r'LOS:.*?(\d+) @', txt).group(1))
            contact = los_timestamp - aos_timestamp +1

            break

# Define the TLE for the satellite

with open(tle, "r") as f:
    x = f.readlines()
    tle_line1 = x[0]
    tle_line2 = x[1]

satellite = twoline2rv(tle_line1, tle_line2, wgs84)

# Define the start time and time step for the calculations
start_time = satellite.epoch
time_step = 1  # Calculate positions every 1 second


longitudes = []
latitudes = []


for i in range(600): ##next X number of seconds
    pos, velocity = satellite.propagate(start_time.year, start_time.month, start_time.day,
                                            start_time.hour, start_time.minute, start_time.second + i*time_step)
    
    lat, lon, alt = ecef2geodetic(pos[0]*1000, pos[1]*1000, pos[2]*1000)

    longitudes.append(lon)
    latitudes.append(lat)


