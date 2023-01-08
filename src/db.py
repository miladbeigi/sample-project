import mysql.connector
import time
import os
import constants
from custom_logging import my_logger


def init_connection():
    not_connected = True
    while not_connected:
        try:
            data_base_connection = mysql.connector.connect(
                host=os.environ.get('MYSQL_HOST', 'localhost'),
                user=os.environ.get('MYSQL_USER', 'root'),
                passwd=os.environ.get(
                    'MYSQL_ROOT_PASSWORD', 'notSecureChangeMe'),
                database=os.environ.get('MYSQL_DEFAULT_DATABASE', 'mysql'))
            not_connected = False
        except:
            my_logger.error(" Connecting to mysql server...")
            time.sleep(constants.WAIT_FOR_DATABASE_SECONDS)
    return data_base_connection, data_base_connection.cursor(dictionary=True)


def check_db_exist():
    data_base_connection, cur = init_connection()

    cur.execute("SHOW DATABASES LIKE 'permissions';")

    myresult = cur.fetchall()

    data_base_connection.commit()
    data_base_connection.close()

    if myresult == []:
        return False
    return True


def write_records(table_name: str, new_records):
    data_base_connection, cur = init_connection()

    table_records = [tuple(record.values()) for record in new_records]

    table_name = f"INSERT INTO permissions.{table_name} "
    values = "VALUES (%s, %s, %s, %s, %s)"

    cur.executemany(table_name+values, table_records)

    data_base_connection.commit()
    data_base_connection.close()


def delete_records(table_name: str):
    data_base_connection, cur = init_connection()

    cur.execute(f"truncate table permissions.{table_name};")
    data_base_connection.commit()
    data_base_connection.close()


def merge_tables():
    data_base_connection, cur = init_connection()

    merge_query = "REPLACE INTO permissions.permission_records SELECT * FROM permissions.permission_records_temp;"

    cur.execute(merge_query)
    data_base_connection.commit()
    data_base_connection.close()


def get_table_records():
    data_base_connection, cur = init_connection()

    cur.execute("SELECT * FROM permissions.permission_records")
    myresult = cur.fetchall()

    data_base_connection.close()
    return myresult


def init_db():
    data_base_connection, cur = init_connection()

    with open('queries/init.sql', 'r') as sql_file:
        result_iterator = cur.execute(sql_file.read(), multi=True)
        for res in result_iterator:
            my_logger.info(" Running query: %s", res)
            my_logger.info(" Affected %s rows", res.rowcount)
        data_base_connection.commit()
    data_base_connection.close()
