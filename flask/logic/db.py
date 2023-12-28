"""Database settings"""
import pymysql
from settings.config import HOST, USER, PASSWORD, DATABASE

def connect_to_database(HOST, USER, PASSWORD, DATABASE):
    connection = pymysql.connect(
        host = HOST,
        user = USER,
        password = PASSWORD,
        database = DATABASE
    )
    return connection

def insert(sql):
    """Execute an INSERT SQL statement passed as a parameter"""
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute(sql)
    cursor.close()
    connection.close()
    return 


def delete(sql):
    """Execute a DELETE SQL statement passed as a parameter"""
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute(sql)
    cursor.close()
    connection.close()
    return


def load(sql):
    """Fetch a row as a result of the given sql statement"""
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    if result:
        return result
    else:
        raise ValueError("No row exists in the DB that corresponds to the provided condition!")

