from DB import *
import pickle

def load_data(database, filename):
    con = conn(database_name=database)
    data = load_database(con, filename)
    with open(f'texts{filename}.pkl', 'ab') as f:
        pickle.dump(data, f)


