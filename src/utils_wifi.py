"""Module that provides all wifi sensor functionality (i.e. returning scan)."""

import os
import pandas as pd
import re
import subprocess


def get_signals():
    """Get wifi signals."""
    operating_system = os.name
    if operating_system == 'nt':
        return get_signals_windows()
    if operating_system == 'posix':
        return get_signals_linux()
    # when here: no matching operating system
    raise Exception('Your operating system ("%s") is not supported. \
                    Currently, windows is supported' % operating_system)


def get_signals_linux():
    """Get wifi signals on linux."""
    command = 'nmcli dev wifi list'
    a = subprocess.check_output(command.split())
    b = str(a)
    bssids = re.findall('[0-9A-Z]{2}:[\wA-Z\:]+', b)
    bssids = [bssid.lower() for bssid in bssids]
    signals = re.findall('MB/s\s+([0-9]+)', b)
    df = pd.DataFrame({'bssid': bssids, 'signal': signals})
    return df


def get_signals_windows():
    """Get wifi signals on windows."""
    command = 'netsh wlan show networks mode=bssid'
    a = subprocess.check_output(command.split(), shell=False)
    b = str(a)
    e = re.findall('[0-9a-z\:]+\:[0-9a-z\:]+', b)
    f = re.findall('(\w+)%', b)
    df = pd.DataFrame({'bssid': e, 'signal': f})
    return df


if __name__ == '__main__':
    print(get_signals())
