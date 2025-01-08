from pymongo import MongoClient


def get_active_table_names():
 
    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    #CONNECTION_STRING = "mongodb://root:example@mongo:27017/datahub_ai"
    
    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient('mongo', 27017, username='root', password='example')

    datahub_ai_db = client['datahub_ai']

    active_tables = datahub_ai_db['active_tables'].find()

    return active_tables