from DB import *
import pickle

def load_data(database, filename):
    con = conn(database_name=database)
    data = load_database(con, filename)
    import pickle

data = {'a': 1, 'b': 2} 

with open(f'{filename}.pkl', 'ab') as f:
   pickle.dump(data, f)
