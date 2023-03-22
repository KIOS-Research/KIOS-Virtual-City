import time

from basp.config import config
import psycopg2
from influxdb import InfluxDBClient


def db_tables_simple_query(query):
    """ PostgreSQL simple query execution """
    conn = None
    try:
        # read connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        # create a cursor
        cur = conn.cursor()
        cur.execute(query)
        # close communication with the PostgreSQL database server
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def update_db_tables(query):
    """ create / delete tables in the PostgreSQL database """
    conn = None
    try:
        # read connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        # create a cursor
        cur = conn.cursor()
        cur.execute(query)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def mod_db_tables(dbtables):
    """ create / delete tables in the PostgreSQL database """
    conn = None
    try:
        # read connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        # create a cursor
        cur = conn.cursor()
        for value in dbtables:
            cur.execute(value)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def mod_db_values(query, data):
    """ modify / add data in the postgresql database """
    conn = None
    try:
        # read connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        # create a cursor
        cur = conn.cursor()
        #if len(data) < 2:
        #    cur.execute(query, data)
        #else:
        cur.executemany(query, data)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def read_db_values(query):
    """ modify / add data in the postgresql database """
    conn = None
    try:
        # read connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        # create a cursor
        cur = conn.cursor()
        cur.execute(query)
        data = cur.fetchall()
        # close communication with the PostgreSQL database server
        cur.close()
        return data
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def read_influxdb_values(query):
    try:
        client = InfluxDBClient(host='influxdb', port=8086, username='kios', password='kios1234!', database='virtual_city')
        data = client.query(str(query))
        client.close()
        results = data.raw
        return results['series'][0]["values"]
    except Exception as error:
        client.close()
        print("Error")
        print(error)


