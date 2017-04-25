# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 19:06:44 2017

@author: DETJENS2
"""

import os
import pandas as pd
import re
import subprocess

def get_signals():
    """Get wifi signals."""
    # TODO: determine operating system
    operating_system = os.name
    if operating_system == 'nt':
        return get_signals_windows()
    # here: no matching operating system
    raise Exception('Your operating system ("%s") is not supported. \
                    Currently, windows is supported' % operating_system)


    def get_signals_windows():
    """Get wifi signals on windows."""
    command = 'netsh wlan show networks mode=bssid'
    a = subprocess.check_output(command.split(), shell=False)
    #a = subprocess.getoutput(command.split())
    b = str(a)
    e = re.findall('[0-9a-z\:]+\:[0-9a-z\:]+', b)
    f = re.findall('(\w+)%', b)
    df = pd.DataFrame({'bssid': e, 'signal': f})
    return df

    
# TODO: get it working for linux
#def get_signals_linux():
#    
#    a = subprocess.check_output(['nmcli', 'dev', 'wifi'])
#    
#    a = str(a)
#    b = str.split(a, '\\n')
#    
#    r1 = [re.findall('[0-9A-Z]{2}:[\wA-Z\:]+', c) for c in b][1:-1]
#    r2 = [re.findall('MB/s\s+(\w+)\s', c) for c in b][1:-1]
#    
#    r3 = [i for [i] in r1]
#    r4 = [i for [i] in r2]
#
#    # TODO: make BSSID lower case
#    # TODO: check if signal strength needs to be transformed
