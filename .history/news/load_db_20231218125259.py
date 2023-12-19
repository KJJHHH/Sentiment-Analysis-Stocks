from DB import *

def load_data(database, filename):
    con = conn(database_name=database)
    data = load_database(con, filename)