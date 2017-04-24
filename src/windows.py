"""
Store wifi signals to SQLite.

@author: DETJENS2
"""

import subprocess
import re
import pandas as pd
import sqlite3
import datetime

# locations that can be logged
locations = ['traveling', 'living_room', 'kitchen', 'bedroom', 'bathroom']
database_path = '../data/wifi.sqlite'


def signals_windows():
    """Get wifi signals on windows."""
    command = 'netsh wlan show networks mode=bssid'
    a = subprocess.check_output(command.split(), shell=False)
    #a = subprocess.getoutput(command.split())
    b = str(a)
    e = re.findall('[0-9a-z\:]+\:[0-9a-z\:]+', b)
    f = re.findall('(\w+)%', b)
    df = pd.DataFrame({'bssid': e, 'signal': f})
    return df


def write_signals_to_db(db=database_path, df=None):
    """Write wifi signals to database."""
    con = sqlite3.connect(db)
    df.to_sql(name='windows', con=con, flavor='sqlite', if_exists='append', index=False)
    con.close()
    

def get_location():
    """Get location from user (options in script parameters)."""
    print('Where are you located?')
    for i in range(0, len(locations)):
        print("%i - %s" % (i, locations[i]))
    k = int(input('location: '))
    return locations[k]
 

def log_signals(db=database_path, location=None):
    """Log current wifi signals."""
    df = signals_windows()
    df['timestamp'] = datetime.datetime.utcnow()
    df['location'] = location    
    write_signals_to_db(db, df)


def log_location():
    """Ask for location and log it, together with current wifi signals."""
    location = get_location()
    print('Logging location "%s" ... ' % location)
    log_signals(location=location)


def read_log_from_db(db=database_path, drop_na=False):
    """Read signal log as dataframe."""
    con = sqlite3.connect(db)
    df = pd.read_sql('SELECT * FROM windows', con=con)
    con.close()
    if drop_na:
        df = df.dropna(axis='index', how='any')  # only complete rows, e.g. w/ locations    
    return df


def get_feature_matrix():
    """
    Create feature matrix from signal log, sorted by timestamp.
    
    Returns only those entries based on complete observations (e.g. having labels).
    """
    df = read_log_from_db(drop_na=True)
    df = df.pivot(index='timestamp', columns='bssid', values='signal')
    df = df.sort_index()
    # NaN to 0
    df = df.fillna(0)
    return df


def get_labels():
    """Return location labels for timestamps."""
    df = read_log_from_db(drop_na=True)
    df = df[['timestamp', 'location']]
    df = df.drop_duplicates()
    df = df.set_index('timestamp')
    df = df.sort_index()
    return df

if __name__ == '__main__':
    # log location
    log_location()
