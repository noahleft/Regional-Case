

from sys import argv
from os import listdir
from os.path import isdir
from re import match

polystring = """
var path = [
polypath];
var polyline = new google.maps.Polyline({path:path, strokeColor: "polycolor", strokeOpacity: 1.0, strokeWeight: 2});
polyline.setMap(map);
"""

maskstring = """
var polygonMask = new google.maps.Polygon({
map:map,
strokeColor: '#000000',
strokeOpacity: 0.5,
strokeWeight: 2,
fillColor: '#CACACA',
fillOpacity: 0.7,
paths: [

	RegionMask
]});
"""

with open('polytemplate.html','r') as infile:
    template = infile.read()

dirlist = [s for s in listdir('.') if 'region' in s and isdir(s)]

def extractLatLng(filepath):
    with open(filepath,'r') as infile:
        strlines = [s.rstrip() for s in infile.readlines()][1:]
    return list(map(lambda x: x.split(','), strlines))

def generatePoly(latlng, color="#FF0000"):
    return polystring.replace("polypath",','.join(['new google.maps.LatLng('+p[0]+','+p[1]+')' for p in latlng])).replace("polycolor",color)

def generateMask(latlng):
    return maskstring.replace('RegionMask',','.join(['new google.maps.LatLng('+p[0]+','+p[1]+')' for p in latlng]))

def calCenter(latlng):
    lats = [float(s[0]) for s in latlng]
    lngs = [float(s[1]) for s in latlng]
    midlat = (max(lats)+min(lats))/2
    midlng = (max(lngs)+min(lngs))/2
    return (midlat, midlng)

colorMap = {"L01":"red","L02":"blue","L03":"black","L04":"green","L05":"brown","L06":"darkgray","L07":"aqua","L08":"darkblue","L09":"darkred","L10":"darkgreen"}

polys = ""
masks = ""
for d in dirlist:
    print('process',d)
    filelist = [s for s in listdir(d) if match(r"R\d+L\d*",s)]
    latlng = []
    for f in filelist:
        if '_' in f or '-' in f:
            tmp = extractLatLng('/'.join([d,f]))[::-1]
            latlng+=tmp
        else:
            color = colorMap[f[f.index('L'):]]
            tmp = extractLatLng('/'.join([d,f]))
            polys+=generatePoly(tmp, color)
            latlng+=tmp
    if d!='region99':
        masks+=generateMask(latlng)

content = template.replace('RegionPoly',polys)
with open('region_poly.html','w') as outfile:
    outfile.write(content)

content = template.replace('RegionPoly',masks)
with open('region_overview.html','w') as outfile:
    outfile.write(content)
