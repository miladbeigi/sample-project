import yaml
import csv
from tabulate import tabulate
import logging
from db import init_db, get_table_records, write_records, delete_records, check_db_exist, merge_tables
import time
import constants
from hash import Hash_File
import os
import sys

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


def read_yaml(path):
    with open(path) as file:
        return yaml.load(file, Loader=yaml.FullLoader)


def main():
    file_path = constants.YAML_FILE_NAME
    yaml_object = read_yaml(file_path)
    return yaml_object


def check_row(csv_records, email):
    for index, line in enumerate(csv_records):
        if email == line['email']:
            return index
    return None


def get_yaml_records():
    yaml_items = read_yaml(constants.YAML_FILE_NAME)

    records = []

    for team in yaml_items['teams']:
        for member in team['members']:
                records.append({
                    'name': member['name'],
                    'email': member['email'],
                    'team': team['name'],
                    'explorer': member['permissions']['explorer'],
                    'sensors': member['permissions']['sensors']
                })
    return records


if __name__ == "__main__":

    check_db_exist = check_db_exist()

    if check_db_exist == False:
        logger.info(" Creating the database")
        init_db()
    else:
        logger.info(" Database exists")

    hash_yaml_file = Hash_File(constants.YAML_FILE_NAME)
    hash_update_file = Hash_File(constants.YAML_FILE_NAME)

    first_run = True

    while True:

        if hash_yaml_file.hash_value == hash_update_file.hash_value and not first_run:
            logger.info(
                " File has not been updated, skipping the database update...")
        else:
            logger.info(" Updating records...")
            table_records = get_table_records()
            yaml_records = get_yaml_records()
            
            delete_records('permission_records_temp')
            write_records('permission_records_temp', yaml_records)
            
            merge_tables()
            
            logger.info(tabulate(get_table_records()))
            hash_yaml_file.update_hash()

        logger.info(" Trying again after %s seconds",
                    constants.RUN_PERIOD_SECONDS)
        time.sleep(constants.RUN_PERIOD_SECONDS)

        logger.info(" Updating the hash....")
        hash_update_file.update_hash()
        first_run = False
