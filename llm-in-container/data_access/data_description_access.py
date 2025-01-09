from pymongo import MongoClient

client = MongoClient('mongo', 27017, username='root', password='example')
datahub_ai_db = client.datahub_ai


def get_active_tables():

    active_tables = datahub_ai_db.active_tables.find()

    return active_tables