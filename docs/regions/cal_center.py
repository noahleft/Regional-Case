#!/usr/bin/python3

from os import listdir

filelist = list(filter(lambda x: x[:6]=='region',listdir('.')))

print(filelist)

import re

for f in filelist:
  with open(f,'r') as infile:
    strlines = infile.readlines()
  print(f, end="\t")
  paths = [line for line in strlines if 'new google.maps.LatLng' in line][5:]
  pattern = re.compile('.*\((\d+\.\d+), (\d+\.\d+)\)')
  lat = list(map(lambda x: float(pattern.match(x).group(1)), paths))
  mean_lat = (max(lat)+min(lat))/2
  lng = list(map(lambda x: float(pattern.match(x).group(2)), paths))
  mean_lng = (max(lng)+min(lng))/2
  print(mean_lat,mean_lng)
  with open(f,'w') as outfile:
    for strline in strlines:
      if "lat:" in strline:
        outfile.write("    lat: "+str(mean_lat)+",\n")
      elif "lng:" in strline:
        outfile.write("    lng: "+str(mean_lng)+"\n")
      else:
        outfile.write(strline)


