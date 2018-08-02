#!/usr/bin/python
 
import psycopg2
from config import config
 
 
def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = (
        """
        CREATE TABLE users (
            user_id SERIAL PRIMARY KEY,
            user_name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL UNIQUE,
            password VARCHAR(255)
        )
        """,
        """ CREATE TABLE diary_entries (
                diary_id SERIAL PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                content VARCHAR(255) NOT NULL,
                owner VARCHAR(255) NOT NULL
                )
        """
        )
    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
 
 
if __name__ == '__main__':
    create_tables()