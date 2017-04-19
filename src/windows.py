"""
Store wifi signals to SQLite.

@author: DETJENS2
"""

import subprocess
import re
import pandas as pd
import sqlite3
import datetime


def add_timestamp_to_df(df):
    """TODO: docstring."""
    df['timestamp'] = datetime.datetime.utcnow()
    return df


def signals_windows():
    """TODO: docstring."""
    command = 'netsh wlan show networks mode=bssid'
    a = subprocess.check_output(command.split(), shell=False)

    b = str(a)
    c = str.split(b, '\\r\\n\\r\\n')

    e = [re.findall('[0-9a-z\:]+\:[0-9a-z\:]+', d) for d in c][1:-1]
    f = [re.findall('(\w+)%', d) for d in c][1:-1]
    e2 = [i for [i] in e]
    f2 = [i for [i] in f]

    df = pd.DataFrame({'bssid': e2, 'signal': f2})

    df = add_timestamp_to_df(df)
    return df


def write_signals_to_db(db='flights.db', df=None):
    """TODO: docstring."""
    con = sqlite3.connect(db)
    df.to_sql(name='test', con=con, flavor='sqlite', if_exists='append',
              index=False)
    con.close()


df = signals_windows()

write_signals_to_db('../data/wifi.sqlite', df)
