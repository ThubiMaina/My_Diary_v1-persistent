
import jwt
from datetime import datetime, timedelta
import psycopg2
from db.config import config


class User:
    """user fields"""
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    @staticmethod
    def generate_token(email):
        try:
            payload = {
            'iss': "mydiary",
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(minutes=30),
            'sub': email
            }
            jwt_string = jwt.encode(payload,
             'secret', algorithm='HS256')
            return jwt_string.decode("utf-8")
        except Exception as e:
            return str(e)

    @staticmethod
    def decode_token(token):
        """Decodes the access token from the authorization header"""
        try:
            payload = jwt.decode(token, 'secret')
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return {"error": "Expired token. Please login to get a new token"}
        except jwt.InvalidTokenError:
            return {"error":"Invalid token. Please register or login"}

    def save(self):
        """ insert a new user into the users table """
        sql = """INSERT INTO users(user_name, password, email)
                 VALUES(%s, %s, %s) RETURNING user_id;"""
        conn = None
        user_id = None
        try:
            # read database configuration
            params = config()
            # connect to the PostgreSQL database
            conn = psycopg2.connect(**params)
            # create a new cursor
            cur = conn.cursor()
            # execute the INSERT statement
            cur.execute(sql, (self.username, self.password, self.email))
            # get the generated id back
            self.user_id = cur.fetchone()[0]
            # commit the changes to the database
            conn.commit()
            # close communication with the database
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print("error", error)
        finally:
            if conn is not None:
                conn.close()
     
        return user_id


    

class DiaryEntries:
    """docstring for DiaryEntries"""
    def __init__(self, user_id, title, date):
        self.user_id = user_id
        self.title = title
        self.date = datetime.utcnow()

    def save_entry(self):
        """ insert a new user into the users table """
        sql = """INSERT INTO diary_entries(user_id, title )
                 VALUES(%s, %s) RETURNING diary_id;"""
        conn = None
        diary_id = None
        

        try:
            # read database configuration
            params = config()
            # connect to the PostgreSQL database
            conn = psycopg2.connect(**params)
            # create a new cursor
            cur = conn.cursor()
            # execute the INSERT statement
            cur.execute(sql, (self.user_id, self.title))
            # get the generated id back
            self.diary_id = cur.fetchone()[0]
            # commit the changes to the database
            conn.commit()
            # close communication with the database
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print("error message", error)
        finally:
            if conn is not None:
                conn.close()
     
        return diary_id

def fetch_entries(user_id = None):
    """ query parts from the parts table """
    conn = None


    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        if user_id is not None:
            cur.execute("SELECT * FROM diary_entries where user_id = " + str(user_id))
        else:
            cur.execute("SELECT * FROM diary_entries")
        rows = cur.fetchall()
        print("The number of entries: ", cur.rowcount)
        for row in rows:
            print(row)
        cur.close()
        return rows
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

