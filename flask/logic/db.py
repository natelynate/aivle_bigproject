"""Database settings"""
import pymysql

def connect_to_database():
    connection = pymysql.connect(
        host='database-1.cjfufsfzm7f6.us-east-1.rds.amazonaws.com',
        user='user1',
        password='Aivle1209',
        database='database-1'
    )
    return connection