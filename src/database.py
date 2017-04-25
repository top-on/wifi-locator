"""
Store wifi signals to SQLite.

@author: DETJENS2
"""

import datetime
import pandas as pd
import sqlite3
import warnings

from wifi_utils import get_signals

# locations that can be logged
locations = ['traveling', 'living_room', 'kitchen', 'bedroom', 'bathroom']
database_path = '../data/wifi.sqlite'
    
    
def get_signal_matrix():
    x = get_feature_matrix()
    df = pd.DataFrame(data=None, columns=x.columns, index=[0])
    df.ix[:,:] = 0
    s = get_signals()
    for bssid in s.bssid:
        if bssid not in df.columns:
            warnings.warn('Ignoring bssid that is not in historic data. \
                          Consider generating more training data with log_location()')
            next
        df.loc[0, bssid] = s[s.bssid == bssid].signal.values[0]
    # if dataframe all zeros, throw exception and inform user
    if (df.values == 0).all():
        raise Exception('None of current wifi hotspots found in training data.')
    return df

    
def write_signals_to_db(db=database_path, df=None):
    """Write wifi signals to database."""
    con = sqlite3.connect(db)
    df.to_sql(name='windows', con=con, if_exists='append', index=False)
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
    df = get_signals()
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
