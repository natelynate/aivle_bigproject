"""This is a place for Database operation related functions"""
import pymysql
from settings.config import HOST, USER, PASSWORD, DATABASE

def connect_to_database(HOST=HOST, USER=USER, PASSWORD=PASSWORD, DATABASE=DATABASE):
    try:
        connection = pymysql.connect(
            host = HOST,
            user = USER,
            password = PASSWORD,
            database = DATABASE
        )
    except:
        return ValueError("Can't establish DB Connection")
    return connection

def insert(sql):
    """Execute an INSERT SQL statement passed as a parameter"""
    connection = connect_to_database(HOST=HOST, USER=USER, PASSWORD=PASSWORD, DATABASE=DATABASE)
    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()
    cursor.close()
    connection.close()
    return "inserted a new row"


def delete(sql):
    """Execute a DELETE SQL statement passed as a parameter"""
    connection = connect_to_database(HOST=HOST, USER=USER, PASSWORD=PASSWORD, DATABASE=DATABASE)
    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()
    cursor.close()
    connection.close()
    return "deleted a row"


def read(sql):
    """Fetch a row as a result of the given sql statement"""
    connection = connect_to_database(HOST=HOST, USER=USER, PASSWORD=PASSWORD, DATABASE=DATABASE)
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    if result:
        return result
    else:
        raise ValueError("No row exists in the DB that corresponds to the provided condition!")


def update(sql):
    """description text"""
    connection = connect_to_database(HOST=HOST, USER=USER, PASSWORD=PASSWORD, DATABASE=DATABASE)
    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()
    cursor.close()
    connection.close()
