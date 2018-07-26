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
                user_id INTEGER ,
                FOREIGN KEY (user_id)
                REFERENCES users (user_id)
                ON UPDATE CASCADE ON DELETE CASCADE
                )
        """,
        """
        CREATE TABLE contents (
                content_id INTEGER PRIMARY KEY,
                contents VARCHAR(255) NOT NULL,
                diary_id INTEGER,
                FOREIGN KEY (diary_id)
                REFERENCES diary_entries (diary_id)
                ON UPDATE CASCADE ON DELETE CASCADE
        )
        """)
    
 
 
if __name__ == '__main__':
    create_tables()