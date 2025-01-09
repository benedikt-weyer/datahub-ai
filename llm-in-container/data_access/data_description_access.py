from pymongo import MongoClient

client = MongoClient('mongo', 27017, username='root', password='example')
datahub_ai_db = client.datahub_ai


def get_active_tables():

    active_tables = datahub_ai_db.active_tables.find()

    return active_tables


def add_table(table_name, description):

    table = {
        'table_name': table_name,
        'table_description': description
    }

    datahub_ai_db.active_tables.insert_one(table)

    return table