from DB import *
import pickle
from fileinput import filename

def load_data(database, filename):
    con = conn(database_name=database)
    data = load_database(con, filename)
    with open(f'texts/{filename}.pkl', 'ab') as f:
        pickle.dump(data, f)

if __name__ == :
    load_data(database, filename)
    print('Done')


