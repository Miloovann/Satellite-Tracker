from sgp4.earth_gravity import wgs84
from sgp4.io import twoline2rv

# Define the TLE for the satellite
tle_line1 = "1 25544U 98067A   21057.98638491  .00003047  00000-0  77314-5 0  9997"
tle_line2 = "2 25544  51.6478  53.3733 0008239  23.6059  53.7333 15.54017469156961"

# Convert the TLE to an SGP4 satellite object
satellite = twoline2rv(tle_line1, tle_line2, wgs84)

# Define the start time and time step for the calculations
start_time = satellite.epoch
time_step = 1  # Calculate positions every 1 second

# Calculate the longitude and latitude of the satellite for the next 10 minutes
longitudes = []
latitudes = []
for i in range(600):  # 10 minutes * 60 seconds/minute = 600 seconds
    # Calculate the position of the satellite at the current time
    position, velocity = satellite.propagate(start_time.year, start_time.month, start_time.day,
                                            start_time.hour, start_time.minute, start_time.second + i*time_step)

    # Extract the longitude and latitude from the position vector
    longitude, latitude, altitude = satellite.eci_to_geodetic(position)

    # Append the longitude and latitude to the lists
    longitudes.append(longitude)
    latitudes.append(latitude)



# At this point, the longitudes and latitudes lists will contain the calculated longitude and latitude values for the satellite, at intervals of 1 second for the next 10 minutes.
