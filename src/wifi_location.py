"""
Get wifi signals on linux.

@author: thor
"""

import subprocess
import re

# linux
a = subprocess.check_output(['nmcli', 'dev', 'wifi'])

a = str(a)
b = str.split(a, '\\n')

r1 = [re.findall('[0-9A-Z]{2}:[\wA-Z\:]+', c) for c in b][1:-1]
r2 = [re.findall('MB/s\s+(\w+)\s', c) for c in b][1:-1]

r3 = [i for [i] in r1]
r4 = [i for [i] in r2]

# TODO: store observations to SQLITE
