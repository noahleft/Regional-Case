
from sys import argv
from os import listdir
from os.path import isdir
from re import match

with open('template.html','r') as infile:
    template = infile.read()

dirlist = [s for s in listdir('.') if 'region' in s and isdir(s)]

borderstring = """
new google.maps.LatLng(24.594715, 120.769917),
new google.maps.LatLng(24.968763, 120.769917),
new google.maps.LatLng(24.968763, 121.217953),
new google.maps.LatLng(24.594715, 121.217953),
new google.maps.LatLng(24.594715, 120.769917)
"""

def extractLatLng(filepath):
    with open(filepath,'r') as infile:
        strlines = [s.rstrip() for s in infile.readlines()][1:]
    return list(map(lambda x: x.split(','), strlines))

def generateMask(latlng):
    return ','.join(['new google.maps.LatLng('+p[0]+','+p[1]+')' for p in latlng])

def calCenter(latlng):
    lats = [float(s[0]) for s in latlng]
    lngs = [float(s[1]) for s in latlng]
    midlat = (max(lats)+min(lats))/2
    midlng = (max(lngs)+min(lngs))/2
    return (midlat, midlng)

filelist = [s for s in listdir('region99') if match(r"R\d+L\d*",s)]
borderlatlng = []
for f in filelist:
    tmp = extractLatLng('/'.join(['region99',f]))
    if '_' in f:
        borderlatlng+=tmp[::-1]
    else:
        borderlatlng+=tmp

for d in dirlist:
    print('process',d)
    filelist = [s for s in listdir(d) if match(r"R\d+L\d*",s)]
    latlng = []
    for f in filelist:
        tmp = extractLatLng('/'.join([d,f]))
        if '_' in f:
            latlng+=tmp[::-1]
        else:
            latlng+=tmp
    if not latlng:
        print(d, 'break')
        break
    content = template.replace('RegionMask',generateMask(latlng[::-1]))
    midlatlng = calCenter(latlng)
    content = content.replace('RegionCeterLat', str(midlatlng[0]))
    content = content.replace('RegionCeterLng', str(midlatlng[1]))
    content = content.replace('RegionalTitle', d)
    if d=='region99':
        content = content.replace('RegionBorder', borderstring)
    else:
        content = content.replace('RegionBorder', generateMask(borderlatlng))
    with open('/'.join([d,d+'.html']),'w') as outfile:
        outfile.write(content)

