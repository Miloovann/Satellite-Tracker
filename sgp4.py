import math

from sgp4.earth_gravity import wgs84
from sgp4.io import twoline2rv
from pymap3d.ecef import ecef2geodetic

tle_line1 = "1 25544U 98067A   21057.98638491  .00003047  00000-0  77314-5 0  9997"
tle_line2 = "2 25544  51.6478  53.3733 0008239  23.6059  53.7333 15.54017469156961"

satellite = twoline2rv(tle_line1, tle_line2, wgs84)

# Define the start time and time step for the calculations
start_time = satellite.epoch
time_step = 1  # Calculate positions every 1 second


longitudes = []
latitudes = []
for i in range(2400): 
    pos, velocity = satellite.propagate(start_time.year, start_time.month, start_time.day,
                                            start_time.hour, start_time.minute, start_time.second + i*time_step)
    
    lat, lon, alt = ecef2geodetic(pos[0]*1000, pos[1]*1000, pos[2]*1000)

    longitudes.append(lon)
    latitudes.append(lat)

print(longitudes)
