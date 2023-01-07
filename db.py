import mysql.connector
import time
import logging
import sys
import os
import constants

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


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
            data_base = mysql.connector.connect(
                host=os.environ.get('MYSQL_HOST', 'localhost'),
                user=os.environ.get('MYSQL_USER', 'root'),
                passwd=os.environ.get(
                    'MYSQL_ROOT_PASSWORD', 'notSecureChangeMe'),
                database=os.environ.get('MYSQL_DEFAULT_DATABASE', 'mysql'))
            not_connected = False
        except:
            logger.error(" Connecting to mysql server...")
            time.sleep(constants.CHECK_FOR_DB_SECONDS)
    return data_base


def write_records(table_name: str, new_records):
    # connecting to the database
    dataBase = init_connection()
    cur = dataBase.cursor(dictionary=True)

    table_records = [tuple(record.values()) for record in new_records]

    table_name = f"INSERT INTO permissions.{table_name} "
    values = "VALUES (%s, %s, %s, %s, %s)"

    cur.executemany(table_name+values, table_records)
    dataBase.commit()


def delete_records(table_name: str):
    dataBase = init_connection()
    cur = dataBase.cursor(dictionary=True)

    cur.execute(f"truncate table permissions.{table_name};")
    dataBase.close()


def merge_tables():
    # connecting to the database
    dataBase = init_connection()
    cur = dataBase.cursor(dictionary=True)

    merge_query = "REPLACE INTO permissions.permission_records SELECT * FROM permissions.permission_records_temp;"

    cur.execute(merge_query)
    dataBase.commit()


def get_table_records():
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
            logger.info(" Running query: %s", res)
            logger.info(" Affected %s rows", res.rowcount)
        dataBase.commit()
    dataBase.close()
