#!/usr/bin/python3


with open('region_all.html','r') as infile:
  strlines = infile.readlines()
  paths = [line for line in strlines if 'new google.maps.LatLng' in line]
  paths = paths[min([idx for idx in range(len(paths)) if paths[idx][0]=='[']):]
  paths = [paths[0][1:-2]+'],\n']+paths[1:-1]+[paths[-1][:-6]+',\n']
  all_regions = paths[::-1]

def replace_border(strlines):
  idx_start = min([idx for idx in range(len(strlines)) if 'paths' in strlines[idx]])
  idx_end   = min([idx for idx in range(len(strlines)) if '[new google.maps.LatLng' in strlines[idx]][1:])
  strlines = strlines[:idx_start] + ['paths: [['] + all_regions + strlines[idx_end:]
  return strlines

from os import listdir

filelist = list(filter(lambda x: x[:6]=='region',listdir('.')))

print(filelist)

import re

for f in filelist:
  with open(f,'r') as infile:
    strlines = infile.readlines()
  paths = [line for line in strlines if 'new google.maps.LatLng' in line]
  paths = paths[min([idx for idx in range(len(paths)) if paths[idx][0]=='[']):]
  pattern = re.compile('.*\((\d+\.\d+), (\d+\.\d+)\)')
  lat = list(map(lambda x: float(pattern.match(x).group(1)), paths))
  mean_lat = (max(lat)+min(lat))/2
  lng = list(map(lambda x: float(pattern.match(x).group(2)), paths))
  mean_lng = (max(lng)+min(lng))/2
  if f != 'region_all.html':
    strlines = replace_border(strlines)
  with open(f,'w') as outfile:
    for strline in strlines:
      if "lat:" in strline:
        outfile.write("    lat: {:.8f},\n".format(mean_lat))
      elif "lng:" in strline:
        outfile.write("    lng: {:.8f}\n".format(mean_lng))
      else:
        outfile.write(strline)




