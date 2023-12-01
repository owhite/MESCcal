#!/usr/bin/env python3

import re

string = """
status json

usb@MESC>{"adc1":0,"ehz":-0.201,"error":0,"id":-0.613,"iq":-0.756,"iqreq":0.000,"TMOS":300.158,"TMOT":211.941,"vbus":31.850,"Vd":-0.205,"Vq":-0.221}
{"adc1":0,"ehz":-0.128,"error":0,"id":-0.639,"iq":-0.774,"iqreq":0.000,"TMOS":300.158,"TMOT":212.057,"vbus":31.925,"Vd":-0.185,"Vq":-0.221}
{"adc1":0,"ehz":-0.067,"error":0,"id":-0.618,"iq":-0.777,"iqreq":0.000,"TMOS":300.158,"TMOT":211.937,"vbus":31.925,"Vd":-0.248,"Vq":-0.221}
{"adc1":0,"ehz":-0.006,"error":0,"id":-0.672,"iq":-0.733,"iqreq":0.000,"TMOS":300.158,"TMOT":211.977,"vbus":31.962,"Vd":-0.227,"Vq":-0.258}
{"adc1":0,"ehz":0.055,"error":0,"id":-0.649,"iq":-0.812,"iqreq":0.000,"TMOS":300.158,"TMOT":211.946,"vbus":31.925,"Vd":-0.206,"Vq":-0.233}
{"adc1":0,"ehz":0.116,"error":0,"id":-0.664,"iq":-0.797,"iqreq":0.000,"TMOS":300.158,"TMOT":211.949,"vbus":31.888,"Vd":-0.227,"Vq":-0.235}
{"adc1":0,"ehz":0.177,"error":0,"id":-0.614,"iq":-0.764,"iqreq":0.000,"TMOS":300.158,"TMOT":212.077,"vbus":31.962,"Vd":-0.184,"Vq":-0.193}
{"adc1":0,"ehz":0.238,"error":0,"id":-0.621,"iq":-0.739,"iqreq":0.000,"TMOS":300.158,"TMOT":211.951,"vbus":31.925,"Vd":-0.226,"Vq":-0.248}
{"adc1":0,"ehz":0.299,"error":0,"id":-0.652,"iq":-0.781,"iqreq":0.000,"TMOS":300.158,"TMOT":211.979,"vbus":31.888,"Vd":-0.206,"Vq":-0.246}
{"adc1":0,"ehz":0.259,"error":0,"id":-0.649,"iq":-0.754,"iqreq":0.000,"TMOS":300.158,"TMOT":211.931,"vbus":31.888,"Vd":-0.227,"Vq":-0.246}
{"adc1":0,"ehz":0.198,"error":0,"id":-0.679,"iq":-0.729,"iqreq":0.000,"TMOS":300.158,"TMOT":211.957,"vbus":31.925,"Vd":-0.227,"Vq":-0.260}
{"adc1":0,"ehz":0.137,"error":0,"id":-0.673,"iq":-0.736,"iqreq":0.000,"TMOS":300.158,"TMOT":212.069,"vbus":31.925,"Vd":-0.226,"Vq":-0.235}
status stop

usb@MESC>
"""

# Define a regular expression pattern to capture text between "{" and "}"
pattern = r'(\{[^}]+\}\n)'
# pattern = r'(\{[^}\"]+\}\n)'

# Find all matches using re.findall
matches = re.findall(pattern, string)

# Concatenate the matches into a single string
text_inside_braces = ''.join(matches)

# Remove the matched substrings from the original string
remaining_text = re.sub(pattern, '', string)

print("BLOCK1")
print(remaining_text)
print("BLOCK2")
print(text_inside_braces)


