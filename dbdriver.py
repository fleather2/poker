import sqlite3
from sqlite3 import Error
from os import path
DATABASE = r"database.db"

def create_connection():
    conn = None
    try:
        con = sqlite3.connect(DATABASE)
        print(sqlite3.version)
    except Error as e:
        print(e)

    finally:
        if conn:
            conn.close() 

def construct_database():


def main():
    if not path.exists(DATABASE):
        create_connection()
        

    

if __name__ == '__main__':
    main()
