import mysql.connector as sq


def connect():
    global con, cursor  # Ensure these are global
    try:
        con = sq.connect(
            host="localhost",
            user="root",
            password="1234",
            database="bus",
            port=3307,
            auth_plugin='mysql_native_password'
        )
        cursor = con.cursor()
        print("Connection to MySQL successful")
        return cursor, con
    except Exception as e:
        print("Connection error:", e)
        return None, None
