
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
        """
        define method to generate token
        """
        try:
            payload = {
            'iss': "mydiary",
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(minutes=600),
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
    def __init__(self, owner, title ,content):
        self.owner = owner
        self.title = title
        self.content = content

    def save_entry(self):
        """ insert a new user into the users table """
        sql = """INSERT INTO diary_entries(owner, title, content )
                 VALUES(%s, %s, %s) RETURNING diary_id;"""
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
            cur.execute(sql, (self.owner, self.title, self.content))
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

    

def delete_entry():
    """ delete an entry by  using the entry_id """
    conn = None


    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the UPDATE  statement
        query = "DELETE FROM diary_entries WHERE diary_id = ('%s')"
        cur.execute(query, [entry_id])
        # Commit the changes to the database
        conn.commit()
        # Close communication with the PostgreSQL database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def fetch_entries(current_user_email):
    """ query entries from the diary entries table """
    conn = None

    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        query = "SELECT * FROM diary_entries where owner = " + ('%s')
        data = str(current_user_email)
        cur.execute(query, [data])
        
        rows = cur.fetchall()
        cur.close()
        return rows
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def get_user(email):
    """ query users from the users table """
    conn = None

    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(" SELECT * FROM users where email = '" + email+ "'")
        rows = cur.fetchall()
        user = None
        if(len(rows)> 0):

            row = rows[0]
            user = User( username=row[1], email=row[2], password=row[3])   
        cur.close()
        
        return user
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()



def update_entry( entry_id,title, content):
        """ update the title of an entry using id """
        sql = """ UPDATE diary_entries
                    SET title = %s, content = %s
                    WHERE diary_id = %s"""
        conn = None
        updated_rows = 0
        try:
            # read database configuration
            params = config()
            # connect to the PostgreSQL database
            conn = psycopg2.connect(**params)
            # create a new cursor
            cur = conn.cursor()
            # execute the UPDATE  statement
            cur.execute(sql, (  title, content, entry_id))
            # get the number of updated rows
            updated_rows = cur.rowcount
            # Commit the changes to the database
            conn.commit()
            # Close communication with the PostgreSQL database
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

        return updated_rows