import sqlite3 as sl
import os
from dotenv import load_dotenv
import requests_country


def db_connection():
    dotenv_path = os.path.join(os.path.dirname(__file__), 'pyth.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
    db_name = os.getenv('bd_tle_NORAD_country')
    con = sl.connect(db_name)
    return con;

def create_table(con: sl.Connection):
    with con:
        con.execute("""
                CREATE TABLE SATELLITES(
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    NAME TEXT,
                    NORAD TEXT,
                    COUNTRY TEXT
                );
        """)

def add_data(satellites: list):
    con = db_connection()
    sql_drop = 'DROP TABLE SATELLITES'
    with con:
        con.execute(sql_drop)

    create_table(con)
    sql = 'INSERT INTO SATELLITES (NAME, NORAD, COUNTRY) values(?, ?, ?)'
    bd_map = []
    for i in range (len(satellites)):
        bd_map.append((satellites[i].name,satellites[i].model.satnum,requests_country.get_country(satellites[i].model.satnum)))
    
    with con:
        con.executemany(sql,bd_map)

def get_sat(name:str,con:sl.Connection):
    with con:
        sat = con.execute("""
                SELECT * FROM SATELLITES WHERE NAME = '%s'""" % name)
    
    return str(sat.fetchall())

