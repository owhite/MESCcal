#!/usr/bin/env python3

import Payload
import re

thing = Payload.Payload()

file1 = open('tmp.txt', 'r')
lines = file1.read()

count = 0
start = False

struct = {}
struct['names'] = []

for line in lines.split('\n'):
    count += 1
    if start: 
        l = line.split('\t')
        if len(l) == 5:
            # print("Line {}: {}".format(line.count('\t'), line.strip()))
            struct[l[0]] = {}
            struct[l[0]]['value'] = l[1]
            struct[l[0]]['min'] = l[2]
            struct[l[0]]['max'] = l[3]
            struct[l[0]]['desc'] = l[4]
            struct['names'].append(l[0])
    if "Parameter\tValue" in line:
        start = True

for l in struct['names']:
    print(l, struct[l]['value'])
