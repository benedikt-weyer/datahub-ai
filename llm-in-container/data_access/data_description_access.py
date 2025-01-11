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

    result = datahub_ai_db.active_tables.insert_one(table)

    return result


def update_table(table_name, description):
    
    result = datahub_ai_db.active_tables.update_one(
        {'table_name': table_name},
        {'$set': {'table_description': description}}
    )

    return result


def remove_table(table_name):
    
    result = datahub_ai_db.active_tables.delete_one({'table_name': table_name})

    return result

def remove_all_tables():
    result = datahub_ai_db.active_tables.delete_many({})
    return result