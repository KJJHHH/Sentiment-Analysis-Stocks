from DB import *
import pickle
import sys
import pandas as pd

"""
cd news
python STORE_FROM_DB.py sentiment_texts -'anue_2409_20231208to20211224'
"""

def load_data(database, filename):
    con = conn(database_name=database)
    data = load_database(con, filename)
    with open(f'texts/{filename}.pkl', 'ab') as f:
        pickle.dump(data, f)

if __name__ == "__main__":
    database, filename = sys.argv[1], sys.argv[2]
    load_data(database, filename)
    print('Done')


