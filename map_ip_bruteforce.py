import re
import gzip
import json
from ip2geotools.databases.noncommercial import Ipstack
import folium

file_path = '/root/auth.log.3.gz'
def parse_log():
  ip_dict = {}
  f = gzip.open(file_path, 'rb')
  log = f.read()
  for line in log.decode().split('\n'):
      if "Failed password for root" in line:
           ips = re.findall(r'(\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b)', line)
           for i in ips: 
               if i not in ip_dict:
                   ip_dict[i] = 1
               else: 
                   ip_dict[i] += 1 
  f.close()       
  return ip_dict

def locate_ip(ip):
    ip_location = Ipstack.get(ip, api_key='example').to_json()
    ip_location = json.loads(ip_location)
    return ip_location

map = folium.Map(location=[31.55294000000002,-5.5607989999999745], zoom_start=6, tiles = "Stamen Terrain")
bg = folium.FeatureGroup(name="Brute_Force map")
ips_list = []
daya = parse_log()
for i in daya: 
    ips_list.append(locate_ip(i))
    for l,j in zip(ips_list,daya):
        l.update(weight = daya[j])

def colors_gen():
    if w < 20:
       return 'green'
    elif 20 <= w < 50:
       return 'orange'
    else:
       return 'red'

for l in ips_list: 
    x = l.get('latitude')
    y = l.get('longitude')
    z = l.get('ip_address')
    w = l.get('weight')
    ips_list = z,str(w)+ ' times'
    bg.add_child(folium.Marker(location=[x,y], popup=ips_list, icon=folium.Icon(color=colors_gen())))
map.add_child(bg)
map.save("bruteforce_map.html")

