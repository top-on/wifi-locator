"""Module that provides all connectivity to SQLite database."""

import datetime
import pandas as pd
import sqlite3

database_path = '../data/wifi.sqlite'


def get_signal_matrix(x, signals):
    """Get signals in the format of a feature matrix, to predict location."""
    df = pd.DataFrame(data=None, columns=x.columns, index=[0])
    df.ix[:, :] = 0
    for bssid in signals.bssid:
        if bssid not in df.columns:
            print('Warning:')
            print('A BSSID is not in historic data. ' +
                  'Consider logging more locations.\n')
            continue
        df.loc[0, bssid] = signals[signals.bssid == bssid].signal.values[0]
    # if dataframe all zeros, throw exception and inform user
    if (df.values == 0).all():
        raise Exception('None of current wifi hotspots in historic data.' +
                        'Please log more locations.')
    return df


def write_signals_to_db(signals, db=database_path):
    """Write wifi signals to database."""
    con = sqlite3.connect(db)
    signals.to_sql(name='windows', con=con, if_exists='append', index=False)
    con.close()


def log_signals(signals, location, db=database_path):
    """Log current wifi signals."""
    signals['timestamp'] = datetime.datetime.utcnow()
    signals['location'] = location
    write_signals_to_db(signals, db)


def read_log_from_db(db=database_path, drop_na=False):
    """Read signal log as dataframe."""
    con = sqlite3.connect(db)
    df = pd.read_sql('SELECT * FROM windows', con=con)
    con.close()
    if drop_na:
        df = df.dropna(axis='index', how='any')  # only rows with locations
    return df


def get_feature_matrix():
    """
    Create feature matrix from signal log, sorted by timestamp.

    Returns only those entries based on observations with locations.
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
