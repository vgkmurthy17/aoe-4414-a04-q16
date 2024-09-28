# ecef_to_sez.py
#
# Usage: python3 ecef_to_sez.py o_x_km o_y_km o_z_km x_km y_km z_km
# Converts ECEF to SEZ
# 
# Parameters:
#  o_x_km (x-coordinate in origin frame)
#  o_y_km (y-coordinate in origin frame)
#  o_z_km (z-coordinate in origin frame)
#  x_km (x ECEF position)
#  y_km (y ECEF position)
#  z_km (z ECEF position)
# Output:
#  Prints the SEZ coordinates in km
#
# Written by Vineet Keshavamurthy
# Other contributors: None
#
# This work is licensed under CC BY-SA 4.0

import sys 
import math


R_E_KM = 6378.1363
E_E = 0.081819221456


def calc_denom(ecc, latitude_rad):
  return math.sqrt(1.0 - ecc ** 2 * math.sin(latitude_rad)**2)

if len(sys.argv) != 7:
    print("Correct Number of Arguments not passed in")
    sys.exit(1)

# input variables
o_x_km = float(sys.argv[1])  # Latitude in degrees
o_y_km = float(sys.argv[2])  # Longitude in degrees
o_z_km = float(sys.argv[3])   # Height above ellipsoid in km
x_km = float(sys.argv[4])       # ECEF x-component in km
y_km = float(sys.argv[5])       # ECEF y-component in km
z_km = float(sys.argv[6])       # ECEF z-component in km


# write script below this line

r_x_km = x_km - o_x_km
r_y_km = y_km - o_y_km
r_z_km = z_km - o_z_km


lon_rad = math.atan2(o_y_km,o_x_km)
lon_deg = lon_rad*180.0/math.pi

# initialize lat_rad, r_lon_km, r_z_km
lat_rad = math.asin(r_z_km/math.sqrt(o_x_km**2+o_y_km**2+o_z_km**2))
r_lon_km = math.sqrt(o_x_km**2+o_y_km**2)
prev_lat_rad = float('nan')

# iteratively find latitude
c_E = float('nan')
count = 0
while (math.isnan(prev_lat_rad) or abs(lat_rad-prev_lat_rad)>10e-7) and count<5:
  denom = calc_denom(E_E,lat_rad)
  c_E = R_E_KM/denom
  prev_lat_rad = lat_rad
  lat_rad = math.atan((o_z_km+c_E*(E_E**2)*math.sin(lat_rad))/r_lon_km)
  count = count+1
  
# calculate hae
hae_km = r_lon_km/math.cos(lat_rad)-c_E

#Complete 1st Rotation
Ry_x = r_x_km * math.cos(lon_rad) + r_y_km * math.sin(lon_rad)

Ry_y = r_x_km * -math.sin(lon_rad) + r_y_km * math.cos(lon_rad)

Ry_z = r_z_km

# Calculate the Rz' matrix 
s_km = Ry_x*math.sin(lat_rad) - Ry_z*(math.cos(lat_rad))

e_km = Ry_y

z_km = Ry_x * math.cos(lat_rad) + Ry_z * math.sin(lat_rad)


print(s_km)
print(e_km)
print(z_km)