# importing required library
import mysql.connector
import time
import logging
import os
   
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def check_db_exist():
    # connecting to the database
    dataBase = init_connection()
    cur = dataBase.cursor(dictionary=True)

    cur.execute("SHOW DATABASES LIKE 'permissions';")

    myresult = cur.fetchall()

    if myresult == []:
        return False
    return True

def init_connection():
    not_connected = True
    while not_connected:
        try:
            dataBase = mysql.connector.connect(
                        host = os.environ['MYSQL_HOST'],
                        user = os.environ['MYSQL_USER'],
                        passwd = os.environ['MYSQL_ROOT_PASSWORD'],
                        database = os.environ['MYSQL_DEFAULT_DATABASE'] )
            not_connected = False
        except:
            logger.error("Trying to connect to mysql server")
            time.sleep(5)
    return dataBase

def write_records(new_records):
    # connecting to the database
    dataBase = init_connection()
    cur = dataBase.cursor(dictionary=True)

    table_records = [tuple(record.values()) for record in new_records] 
    
    insert_query = """
        INSERT INTO permissions.permission_records
        VALUES (%s, %s, %s, %s, %s)
        """
    
    cur.executemany(insert_query, table_records)
    dataBase.commit()

def delete_records():
    dataBase = init_connection()
    cur = dataBase.cursor(dictionary=True)
    
    cur.execute("truncate table permissions.permission_records;")
    dataBase.close()

def get_records():
    # connecting to the database
    dataBase = init_connection()
    cur = dataBase.cursor(dictionary=True)

    cur.execute("SELECT * FROM permissions.permission_records")
    myresult = cur.fetchall()
    
    dataBase.close()
    return myresult


def init_db():  
    
    # connecting to the database
    dataBase = init_connection()
    cur = dataBase.cursor(dictionary=True)

    with open('queries/init.sql', 'r') as sql_file:
        result_iterator = cur.execute(sql_file.read(), multi=True)
        for res in result_iterator:
            print("Running query: ", res)
            print(f"Affected {res.rowcount} rows" )
        dataBase.commit()
    dataBase.close()