#!/usr/local/bin/python3

import json

d = {}
d['colors'] = []
with open("name_hex_rgb.txt", 'r') as f:
	for line in f.readlines():
		line = line.split()
		d['colors'].append({line[1] :{'name' : line[0], 'rgb' : line[2]}})

with open('color.json', 'w') as o:
    json.dump(d, o)

