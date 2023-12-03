#!/usr/bin/env python3

import json

file_path = "tab_contents.json"
try:
    with open(file_path, 'r') as json_file:
        try:
            tab_data = json.load(json_file)

        except json.JSONDecodeError as json_error:
            print(f"Error decoding JSON: {json_error}")

except FileNotFoundError:
    print(f"Error: The file '{file_path}' does not exist.")

for t in tab_data.keys():
    print ("name: {0}".format(t))
    print ("title: {0}".format(tab_data[t]['title']))
    tab_dict = tab_data[t]
    boxes = tab_data[t]['boxes']

    for box in boxes:
        print ("box: {0}".format(box['name']))
        rows = box['buttons']
        print(rows)
        for row in rows:
            print("row")
            for r in row:
                print(r)
            # print ("button: {0}".format(r['name']))
