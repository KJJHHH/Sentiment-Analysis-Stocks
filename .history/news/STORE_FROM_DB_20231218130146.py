from DB import *
import pickle
import sys

def load_data(database, filename):
    con = conn(database_name=database)
    data = load_database(con, filename)
    with open(f'texts/{filename}.pkl', 'ab') as f:
        pickle.dump(data, f)

if __name__ == "__main__":
    database, fil = sys.argv[1]
    filename = sys.argv[2]
    load_data(database, filename)
    print('Done')


